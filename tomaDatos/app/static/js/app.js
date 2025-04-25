// app.py - Para Flask tradicional

const { Flask } = require('flask');
const path = require('path');

// Crear aplicación Flask
const app = new Flask(__name__);

// Configuración básica
app.config.from_pyfile('config.py');

// Configurar rutas de templates y static files
app.template_folder = path.join(__dirname, 'templates');
app.static_folder = path.join(__dirname, 'static');

// Registrar blueprints
const main_bp = require('./routes/main_routes');
app.register_blueprint(main_bp);

// Manejo de errores
app.errorhandler(404, (error) => {
  return app.render_template('errors/404.html'), 404;
});

app.errorhandler(500, (error) => {
  return app.render_template('errors/500.html'), 500;
});

// Iniciar servidor
if (require.main === module) {
  const PORT = process.env.PORT || 5000;
  app.run({
    port: PORT,
    debug: process.env.FLASK_ENV === 'development',
    host: '0.0.0.0'
  });
}

module.exports = app;