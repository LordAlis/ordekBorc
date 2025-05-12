from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.user import db, User
from models.transaction import Transaction
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ordekborc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    total_lent = sum(t.amount for t in transactions if not t.is_paid)
    return render_template('dashboard.html', 
                         transactions=transactions,
                         total_lent=total_lent)

@app.route('/new_transaction', methods=['GET', 'POST'])
@login_required
def new_transaction():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        description = request.form.get('description')
        borrower_name = request.form.get('borrower_name')
        
        transaction = Transaction(
            amount=amount,
            description=description,
            borrower_name=borrower_name,
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        
        flash('Transaction recorded successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('new_transaction.html')

@app.route('/mark_as_paid/<int:transaction_id>')
@login_required
def mark_as_paid(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    
    if transaction.user_id != current_user.id:
        flash('Unauthorized action')
        return redirect(url_for('dashboard'))
    
    transaction.is_paid = True
    transaction.paid_at = datetime.utcnow()
    db.session.commit()
    flash('Transaction marked as paid!')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
