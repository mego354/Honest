from flask import Flask, request, render_template, redirect, flash, jsonify, abort
import sqlite3
from datetime import datetime, date
import json
from contextlib import contextmanager
import logging
import os

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'مفتاح_سري_قوي_للغاية_2024'  # يجب تغييره في الإنتاج
app.config['JSON_AS_ASCII'] = False  # لدعم العربية في JSON

# تأكد من وجود مجلد للملفات
if not os.path.exists('instance'):
    os.makedirs('instance')

DATABASE = 'instance/inventory.db'

@contextmanager
def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    with get_db_connection() as conn:
        c = conn.cursor()
        
        # جدول الموديلات
        c.execute('''CREATE TABLE IF NOT EXISTS models
                     (model_number TEXT PRIMARY KEY,
                      items_per_carton INTEGER NOT NULL,
                      creation_date TEXT NOT NULL,
                      status TEXT DEFAULT 'active')''')
        
        # جدول المخزون
        c.execute('''CREATE TABLE IF NOT EXISTS inventory
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      model_number TEXT,
                      part_number INTEGER,
                      part_type TEXT,
                      size TEXT,
                      total_quantity INTEGER,
                      produced_quantity INTEGER DEFAULT 0,
                      last_update TEXT,
                      FOREIGN KEY (model_number) REFERENCES models(model_number) ON DELETE CASCADE,
                      UNIQUE(model_number, part_number, size))''')
        
        # جدول سجلات الإنتاج
        c.execute('''CREATE TABLE IF NOT EXISTS production_logs
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT NOT NULL,
                      factory TEXT NOT NULL,
                      model_number TEXT NOT NULL,
                      part_number INTEGER NOT NULL,
                      part_type TEXT NOT NULL,
                      size TEXT NOT NULL,
                      quantity INTEGER NOT NULL,
                      created_at TEXT NOT NULL,
                      notes TEXT,
                      FOREIGN KEY (model_number) REFERENCES models(model_number) ON DELETE CASCADE)''')
        
        # جدول سجلات التعبئة
        c.execute('''CREATE TABLE IF NOT EXISTS packing_logs
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT NOT NULL,
                      model_number TEXT NOT NULL,
                      cartons_packed INTEGER NOT NULL,
                      created_at TEXT NOT NULL,
                      notes TEXT,
                      FOREIGN KEY (model_number) REFERENCES models(model_number) ON DELETE CASCADE)''')
        
        conn.commit()

def get_model_details(model_number):
    """جلب تفاصيل موديل معين بشكل مفصل"""
    with get_db_connection() as conn:
        c = conn.cursor()
        
        # التحقق من وجود الموديل
        c.execute('''SELECT model_number, items_per_carton, creation_date, status 
                     FROM models 
                     WHERE model_number = ?''', (model_number,))
        model = c.fetchone()
        
        if not model:
            return None
            
        # جلب تفاصيل القطع مع معلومات الإنتاج والتعبئة التفصيلية
        c.execute('''SELECT 
                        i.part_number, 
                        i.part_type, 
                        i.size, 
                        i.total_quantity, 
                        i.produced_quantity,
                        (SELECT COALESCE(SUM(quantity), 0) 
                         FROM production_logs 
                         WHERE model_number = ? AND part_number = i.part_number AND size = i.size) as total_production,
                        (SELECT COALESCE(SUM(cartons_packed), 0) 
                         FROM packing_logs 
                         WHERE model_number = ?) as total_packing
                     FROM inventory i
                     WHERE i.model_number = ?
                     ORDER BY i.part_number, i.size''', 
                     (model_number, model_number, model_number))
        
        inventory_items = c.fetchall()
        
        # جلب سجلات الإنتاج التفصيلية
        c.execute('''SELECT date, factory, part_type, size, quantity, notes
                     FROM production_logs
                     WHERE model_number = ?
                     ORDER BY date DESC''', (model_number,))
        production_logs = c.fetchall()
        
        # جلب سجلات التعبئة التفصيلية
        c.execute('''SELECT date, cartons_packed, notes
                     FROM packing_logs
                     WHERE model_number = ?
                     ORDER BY date DESC''', (model_number,))
        packing_logs = c.fetchall()
        
        parts = {}
        
        for item in inventory_items:
            part_number = item['part_number']
            if part_number not in parts:
                parts[part_number] = {
                    'type': item['part_type'],
                    'sizes': [],
                }
            
            remaining = item['total_quantity'] - item['produced_quantity']
            parts[part_number]['sizes'].append({
                'size': item['size'],
                'total': item['total_quantity'],
                'produced': item['produced_quantity'],
                'total_production': item['total_production'],
                'remaining': remaining
            })
        
        return {
            'model_info': dict(model),
            'parts': [{'part_number': k, **v} for k, v in parts.items()],
            'production_logs': production_logs,
            'packing_logs': packing_logs
        }

def calculate_model_status(model_number):
    """حساب حالة الموديل الحالية بشكل شامل"""
    with get_db_connection() as conn:
        c = conn.cursor()
        
        # حساب إجمالي القطع والكراتين بتفاصيل أكثر
        c.execute('''SELECT 
                        m.items_per_carton,
                        m.creation_date,
                        m.status,
                        (SELECT COALESCE(SUM(total_quantity), 0) FROM inventory 
                         WHERE model_number = m.model_number) as total_pieces,
                        (SELECT COALESCE(SUM(produced_quantity), 0) FROM inventory 
                         WHERE model_number = m.model_number) as total_produced,
                        (SELECT COALESCE(COUNT(DISTINCT part_number), 0) FROM inventory 
                         WHERE model_number = m.model_number) as total_part_types
                    FROM models m
                    WHERE m.model_number = ?''', (model_number,))
        
        result = c.fetchone()
        if not result:
            return None
        
        # حساب الكراتين
        total_cartons = result['total_pieces'] // result['items_per_carton'] if result['items_per_carton'] > 0 else 0
        
        # إحصائيات الإنتاج
        c.execute('''SELECT 
                        COALESCE(SUM(quantity), 0) as total_production_qty,
                        COUNT(DISTINCT factory) as factories_count,
                        MIN(date) as first_production_date,
                        MAX(date) as last_production_date
                     FROM production_logs
                     WHERE model_number = ?''', (model_number,))
        
        production_stats = c.fetchone()
        
        # إحصائيات التعبئة
        c.execute('''SELECT 
                        COALESCE(SUM(cartons_packed), 0) as total_packed,
                        MIN(date) as first_packing_date,
                        MAX(date) as last_packing_date
                     FROM packing_logs
                     WHERE model_number = ?''', (model_number,))
        
        packing_stats = c.fetchone()
        
        return {
            'total_pieces': result['total_pieces'],
            'produced_pieces': result['total_produced'],
            'total_cartons': total_cartons,
            'packed_cartons': packing_stats['total_packed'] // result['items_per_carton'] if result['items_per_carton'] > 0 else 0,
            'remaining_cartons': max(0, total_cartons - (packing_stats['total_packed'] // result['items_per_carton'] if result['items_per_carton'] > 0 else 0)),
            'items_per_carton': result['items_per_carton'],
            'status': result['status'],
            'creation_date': result['creation_date'],
            'production_stats': dict(production_stats),
            'packing_stats': dict(packing_stats)
        }

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            # جلب قائمة الموديلات النشطة
            c.execute('''SELECT m.model_number, m.items_per_carton, m.creation_date, m.status
                         FROM models m
                         WHERE m.status = 'active'
                         ORDER BY m.creation_date DESC''')
            models = c.fetchall()
            
            # حساب حالة كل موديل
            model_statuses = {}
            for model in models:
                model_number = model['model_number']
                details = get_model_details(model_number)
                status = calculate_model_status(model_number)
                
                if details and status:
                    model_statuses[model_number] = {
                        'details': details,
                        'status': status
                    }
            
            return render_template('index.html', models=model_statuses)
                                 
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        flash('حدث خطأ أثناء تحميل البيانات', 'danger')
        return redirect('/error')

@app.route('/add_model', methods=['POST'])
def add_model():
    """إضافة موديل جديد"""
    try:
        model_number = request.form['model_number'].strip()
        items_per_carton = int(request.form['items_per_carton'])
        
        # التحقق من وجود القطع والمقاسات
        part_types = request.form.getlist('part_types[]')
        sizes = request.form.getlist('sizes[]')
        quantities = [int(q) for q in request.form.getlist('quantities[]')]
        
        # التحقق من صحة البيانات
        if not all([model_number, items_per_carton, part_types, sizes, quantities]):
            flash('جميع الحقول مطلوبة', 'danger')
            return redirect('/')
            
        if any(q <= 0 for q in quantities):
            flash('يجب أن تكون جميع الكميات أكبر من صفر', 'danger')
            return redirect('/')
            
        with get_db_connection() as conn:
            c = conn.cursor()
            
            # التحقق من عدم وجود الموديل
            c.execute('SELECT 1 FROM models WHERE model_number = ?', (model_number,))
            if c.fetchone():
                flash('هذا الموديل موجود بالفعل', 'danger')
                return redirect('/')
            
            # إضافة الموديل
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''INSERT INTO models 
                         (model_number, items_per_carton, creation_date, status)
                         VALUES (?, ?, ?, 'active')''', 
                         (model_number, items_per_carton, now))
            
            # إضافة المخزون
            for idx, (part_type, size, quantity) in enumerate(zip(part_types, sizes, quantities), 1):
                c.execute('''INSERT INTO inventory 
                           (model_number, part_number, part_type, size, 
                           total_quantity, produced_quantity, last_update)
                           VALUES (?, ?, ?, ?, ?, 0, ?)''',
                           (model_number, idx, part_type, size, quantity, now))
            
            conn.commit()
            flash('تم إضافة الموديل بنجاح', 'success')
            
    except sqlite3.IntegrityError:
        flash('حدث خطأ في البيانات. يرجى التحقق من عدم تكرار المقاسات', 'danger')
    except ValueError as e:
        flash(f'خطأ في البيانات: {str(e)}', 'danger')
    except Exception as e:
        logger.error(f"Error in add_model: {str(e)}")
        flash('حدث خطأ أثناء إضافة الموديل', 'danger')
        
    return redirect('/')

@app.route('/production', methods=['POST'])
def add_production():
    """تسجيل إنتاج جديد"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            data = request.form
            model_number = data['model_number']
            part_number = int(data['part_number'])
            quantity = int(data['quantity'])
            
            # التحقق من حالة الموديل
            c.execute('SELECT status FROM models WHERE model_number = ?', (model_number,))
            model_status = c.fetchone()
            if not model_status or model_status['status'] != 'active':
                flash('هذا الموديل غير نشط أو غير موجود', 'danger')
                return redirect('/')
            
            # التحقق من الكمية المتبقية
            c.execute('''SELECT total_quantity, produced_quantity 
                         FROM inventory 
                         WHERE model_number = ? AND part_number = ? AND size = ?''',
                     (model_number, part_number, data['size']))
            
            inv = c.fetchone()
            if not inv:
                flash('لم يتم العثور على القطعة المحددة', 'danger')
                return redirect('/')
                
            remaining = inv['total_quantity'] - inv['produced_quantity']
            if quantity > remaining:
                flash(f'الكمية المطلوبة ({quantity}) أكبر من المتبقي ({remaining})', 'danger')
                return redirect('/')
            
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # تحديث المخزون
            c.execute('''UPDATE inventory 
                         SET produced_quantity = produced_quantity + ?,
                             last_update = ?
                         WHERE model_number = ? AND part_number = ? AND size = ?''',
                     (quantity, now, model_number, part_number, data['size']))
            
            # إضافة سجل الإنتاج
            notes = data.get('notes', '')
            c.execute('''INSERT INTO production_logs 
                         (date, factory, model_number, part_number, part_type, size, quantity, created_at, notes)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (data['date'], data['factory'], model_number, part_number,
                      data['part_type'], data['size'], quantity, now, notes))
            
            conn.commit()
            flash('تم تسجيل الإنتاج بنجاح', 'success')
            
    except ValueError as e:
        flash(f'خطأ في البيانات: {str(e)}', 'danger')
    except Exception as e:
        logger.error(f"Error in add_production: {str(e)}")
        flash('حدث خطأ أثناء تسجيل الإنتاج', 'danger')
        
    return redirect('/')

@app.route('/add_packing', methods=['POST'])
def add_packing():
    """تسجيل تعبئة جديدة"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            data = request.form
            model_number = data['model_number']
            cartons_packed = int(data['cartons_packed'])
            
            # التحقق من حالة الموديل
            c.execute('SELECT status FROM models WHERE model_number = ?', (model_number,))
            model_status = c.fetchone()
            if not model_status or model_status['status'] != 'active':
                flash('هذا الموديل غير نشط أو غير موجود', 'danger')
                return redirect('/')
            
            # التحقق من الكراتين المتبقية
            status = calculate_model_status(model_number)
            if not status:
                flash('لم يتم العثور على الموديل', 'danger')
                return redirect('/')
                
            if cartons_packed > status['remaining_cartons']:
                flash(f'عدد الكراتين المطلوب ({cartons_packed}) أكبر من المتبقي ({status["remaining_cartons"]})', 'danger')
                return redirect('/')
            
            # إضافة سجل التعبئة
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            notes = data.get('notes', '')
            c.execute('''INSERT INTO packing_logs 
                         (date, model_number, cartons_packed, created_at, notes)
                         VALUES (?, ?, ?, ?, ?)''',
                     (data['date'], model_number, cartons_packed, now, notes))
            
            conn.commit()
            flash('تم تسجيل التعبئة بنجاح', 'success')
            
    except ValueError as e:
        flash(f'خطأ في البيانات: {str(e)}', 'danger')
    except Exception as e:
        logger.error(f"Error in add_packing: {str(e)}")
        flash('حدث خطأ أثناء تسجيل التعبئة', 'danger')
        
    return redirect('/')

@app.route('/api/model_details/<model_number>')
def get_model_details_api(model_number):
    """واجهة برمجية لجلب تفاصيل الموديل"""
    try:
        details = get_model_details(model_number)
        if not details:
            return jsonify({'error': 'Model not found'}), 404
        return jsonify(details)
    except Exception as e:
        logger.error(f"Error in get_model_details_api: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/part_sizes/<model_number>/<int:part_number>')
def get_part_sizes_api(model_number, part_number):
    """واجهة برمجية لجلب مقاسات القطعة"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            c.execute('''SELECT size, total_quantity, produced_quantity 
                         FROM inventory 
                         WHERE model_number = ? AND part_number = ?
                         ORDER BY size''', (model_number, part_number))
            
            sizes = []
            for row in c.fetchall():
                remaining = row['total_quantity'] - row['produced_quantity']
                sizes.append({
                    'size': row['size'],
                    'total': row['total_quantity'],
                    'produced': row['produced_quantity'],
                    'remaining': remaining
                })
            
            if not sizes:
                return jsonify({'error': 'Part not found'}), 404
                
            return jsonify({'sizes': sizes})
            
    except Exception as e:
        logger.error(f"Error in get_part_sizes_api: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/factory_production', methods=['POST'])
def get_factory_production():
    """واجهة برمجية لجلب إنتاج المصنع"""
    try:
        factory = request.form.get('factory', '')
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')
        
        with get_db_connection() as conn:
            c = conn.cursor()
            
            query = '''SELECT p.date, p.model_number, p.part_type, p.size, 
                             SUM(p.quantity) as total_quantity,
                             m.status as model_status
                      FROM production_logs p
                      JOIN models m ON p.model_number = m.model_number
                      WHERE p.factory LIKE ?'''
            params = ['%' + factory + '%']
            
            if start_date and end_date:
                query += ' AND p.date BETWEEN ? AND ?'
                params.extend([start_date, end_date])
                
            query += ''' GROUP BY p.date, p.model_number, p.part_type, p.size
                        ORDER BY p.date DESC'''
            
            c.execute(query, params)
            results = c.fetchall()
            
            production_summary = {
                'total_quantity': sum(row['total_quantity'] for row in results),
                'details': [dict(row) for row in results]
            }
            
            return jsonify(production_summary)
            
    except Exception as e:
        logger.error(f"Error in get_factory_production: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/update_model_size', methods=['POST'])
def update_model_size():
    """تحديث كمية المقاس"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            model_number = request.form['model_number']
            part_number = int(request.form['part_number'])
            size = request.form['size']
            new_total = int(request.form['total_quantity'])
            
            # التحقق من الكمية المنتجة الحالية
            c.execute('''SELECT produced_quantity 
                         FROM inventory 
                         WHERE model_number = ? AND part_number = ? AND size = ?''',
                     (model_number, part_number, size))
            
            current = c.fetchone()
            if not current:
                return jsonify({'error': 'Size not found'}), 404
                
            if new_total < current['produced_quantity']:
                return jsonify({
                    'error': 'New total quantity cannot be less than produced quantity'
                }), 400
            
            # تحديث الكمية
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''UPDATE inventory 
                         SET total_quantity = ?, last_update = ?
                         WHERE model_number = ? AND part_number = ? AND size = ?''',
                     (new_total, now, model_number, part_number, size))
            
            conn.commit()
            return jsonify({'success': True})
            
    except Exception as e:
        logger.error(f"Error in update_model_size: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/delete_production_log/<int:log_id>', methods=['POST'])
def delete_production_log(log_id):
    """حذف سجل إنتاج"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            # استرجاع تفاصيل السجل قبل الحذف
            c.execute('''SELECT model_number, part_number, size, quantity 
                         FROM production_logs 
                         WHERE id = ?''', (log_id,))
            
            log = c.fetchone()
            if not log:
                return jsonify({'error': 'Log not found'}), 404
            
            # تحديث المخزون
            c.execute('''UPDATE inventory 
                         SET produced_quantity = produced_quantity - ?,
                             last_update = ?
                         WHERE model_number = ? AND part_number = ? AND size = ?''',
                     (log['quantity'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                      log['model_number'], log['part_number'], log['size']))
            
            # حذف السجل
            c.execute('DELETE FROM production_logs WHERE id = ?', (log_id,))
            
            conn.commit()
            flash('تم حذف سجل الإنتاج بنجاح', 'success')
            return jsonify({'success': True})
            
    except Exception as e:
        logger.error(f"Error in delete_production_log: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/delete_packing_log/<int:log_id>', methods=['POST'])
def delete_packing_log(log_id):
    """حذف سجل تعبئة"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            c.execute('DELETE FROM packing_logs WHERE id = ?', (log_id,))
            
            if c.rowcount == 0:
                return jsonify({'error': 'Log not found'}), 404
            
            conn.commit()
            flash('تم حذف سجل التعبئة بنجاح', 'success')
            return jsonify({'success': True})
            
    except Exception as e:
        logger.error(f"Error in delete_packing_log: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/deactivate_model/<model_number>', methods=['POST'])
def deactivate_model(model_number):
    """إلغاء تفعيل موديل"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            c.execute('''UPDATE models 
                         SET status = 'inactive'
                         WHERE model_number = ?''', (model_number,))
            
            if c.rowcount == 0:
                return jsonify({'error': 'Model not found'}), 404
            
            conn.commit()
            flash('تم إلغاء تفعيل الموديل بنجاح', 'success')
            return jsonify({'success': True})
            
    except Exception as e:
        logger.error(f"Error in deactivate_model: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/error')
def error():
    """صفحة الخطأ"""
    return render_template('error.html')

@app.errorhandler(404)
def not_found_error(error):
    """معالج أخطاء 404"""
    return render_template('error.html', error='الصفحة غير موجودة'), 404

@app.errorhandler(500)
def internal_error(error):
    """معالج أخطاء 500"""
    return render_template('error.html', error='خطأ في الخادم'), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8000)