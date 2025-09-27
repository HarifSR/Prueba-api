// index.js

// 1. Importaciones
const express = require('express');
const sql = require('mssql');
require('dotenv').config(); // Carga las variables del archivo .env

// 2. Configuración de la aplicación
const app = express();
app.use(express.json()); // Middleware para entender JSON

// 3. Configuración de la conexión a la base de datos
const dbConfig = {
    user: process.env.DB_USERNAME,
    password: process.env.DB_PASSWORD,
    server: process.env.DB_SERVER,
    database: process.env.DB_DATABASE,
    options: {
        encrypt: true, // Requerido para Azure
        trustServerCertificate: true // Cambiar a false para producción con certificados válidos
    }
};

// 4. Endpoints de la API

// =================== PRODUCTOS ===================

// GET: Obtener todos los productos
app.get('/productos', async (req, res) => {
    try {
        // Conectarse a la base de datos
        let pool = await sql.connect(dbConfig);
        // Ejecutar la consulta
        let result = await pool.request().query('SELECT * FROM dbo.Productos');
        // Enviar el resultado
        res.status(200).json(result.recordset);
    } catch (err) {
        // Manejo de errores
        console.error(err);
        res.status(500).send({ mensaje: 'Error al conectar a la base de datos', error: err });
    }
});

// POST: Guardar un nuevo producto
app.post('/productos', async (req, res) => {
    // Obtenemos los datos del cuerpo de la petición
    const { ProductoID, Nombre, Descripcion, Precio, CategoriaID } = req.body;

    // Validamos que los datos necesarios estén presentes
    if (!ProductoID || !Nombre || !Precio) {
        return res.status(400).json({ mensaje: 'ProductoID, Nombre y Precio son campos requeridos.' });
    }

    try {
        let pool = await sql.connect(dbConfig);
        await pool.request()
            // Usamos parámetros para prevenir inyección SQL (¡muy importante!)
            .input('ProductoID', sql.VarChar, ProductoID)
            .input('Nombre', sql.NVarChar, Nombre)
            .input('Descripcion', sql.NVarChar, Descripcion)
            .input('Precio', sql.Decimal(18, 2), Precio)
            .input('CategoriaID', sql.Int, CategoriaID)
            .query('INSERT INTO dbo.Productos (ProductoID, Nombre, Descripcion, Precio, CategoriaID) VALUES (@ProductoID, @Nombre, @Descripcion, @Precio, @CategoriaID)');

        // Devolvemos una respuesta de éxito con los datos insertados
        res.status(201).json({ ProductoID, Nombre, Descripcion, Precio, CategoriaID });
    } catch (err) {
        console.error(err);
        res.status(500).send({ mensaje: 'Error al guardar el producto', error: err });
    }
});


// =================== VEHÍCULOS ===================

// GET: Obtener todos los vehículos
app.get('/vehiculos', async (req, res) => {
    try {
        let pool = await sql.connect(dbConfig);
        let result = await pool.request().query('SELECT * FROM dbo.Vehiculos');
        res.status(200).json(result.recordset);
    } catch (err) {
        console.error(err);
        res.status(500).send({ mensaje: 'Error al obtener los vehículos', error: err });
    }
});


// 5. Iniciar el servidor
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`Servidor corriendo en el puerto ${PORT}`);
});