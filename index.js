// index.js

const express = require('express');
const sql = require('mssql');
require('dotenv').config();
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// Config DB
const dbConfig = {
  user: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD,
  server: process.env.DB_SERVER,
  database: process.env.DB_DATABASE,
  options: {
    encrypt: true,
    trustServerCertificate: true
  }
};

// Config Swagger
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'API de Productos y Vehículos',
      version: '1.0.0',
      description: 'Una API simple para gestionar productos y vehículos, documentada con Swagger.'
    },
    servers: [
      {
        url: 'https://prueba-api-zd2m.onrender.com',
        description: 'Servidor de Desarrollo'
      }
    ]
  },
  apis: [path.join(__dirname, '*.js')],
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));


// =================== TAGS ===================

/**
 * @swagger
 * tags:
 *   - name: Productos
 *     description: Endpoints para gestionar productos
 *   - name: Vehículos
 *     description: Endpoints para gestionar vehículos
 */



// =================== PRODUCTOS ===================

/**
 * @swagger
 * /productos:
 *   get:
 *     summary: Retorna una lista de todos los productos
 *     tags: [Productos]
 *     responses:
 *       '200':
 *         description: Lista de productos obtenida exitosamente
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *   post:
 *     summary: Crea un nuevo producto
 *     tags: [Productos]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             example:
 *               ProductoID: "P123"
 *               Nombre: "Nuevo Producto"
 *               Descripcion: "Descripción de ejemplo"
 *               Precio: 19.99
 *               CategoriaID: 1
 *     responses:
 *       '201':
 *         description: Producto creado exitosamente
 */
app.get('/productos', async (req, res) => {
  try {
    let pool = await sql.connect(dbConfig);
    let result = await pool.request().query('SELECT * FROM dbo.Productos');
    res.status(200).json(result.recordset);
  } catch (err) {
    res.status(500).send({ mensaje: 'Error al obtener los productos', error: err });
  }
});

app.post('/productos', async (req, res) => {
  const { ProductoID, Nombre, Descripcion, Precio, CategoriaID } = req.body;
  if (!ProductoID || !Nombre || !Precio) {
    return res.status(400).json({ mensaje: 'ProductoID, Nombre y Precio son campos requeridos.' });
  }
  try {
    let pool = await sql.connect(dbConfig);
    await pool.request()
      .input('ProductoID', sql.VarChar, ProductoID)
      .input('Nombre', sql.NVarChar, Nombre)
      .input('Descripcion', sql.NVarChar, Descripcion)
      .input('Precio', sql.Decimal(18, 2), Precio)
      .input('CategoriaID', sql.Int, CategoriaID)
      .query('INSERT INTO dbo.Productos (ProductoID, Nombre, Descripcion, Precio, CategoriaID) VALUES (@ProductoID, @Nombre, @Descripcion, @Precio, @CategoriaID)');
    res.status(201).json({ ProductoID, Nombre, Descripcion, Precio, CategoriaID });
  } catch (err) {
    res.status(500).send({ mensaje: 'Error al guardar el producto', error: err });
  }
});

// =================== VEHÍCULOS ===================

/**
 * @swagger
 * /vehiculos:
 *   get:
 *     summary: Retorna una lista de todos los vehículos
 *     tags: [Vehículos]
 *     responses:
 *       '200':
 *         description: Lista de vehículos obtenida exitosamente
 *   post:
 *     summary: Crea un nuevo vehículo
 *     tags: [Vehículos]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             example:
 *               modelo: "Corolla"
 *               marca: "Toyota"
 *               linea: "Sedán"
 *     responses:
 *       '201':
 *         description: Vehículo creado exitosamente
 */
app.get('/vehiculos', async (req, res) => {
  try {
    let pool = await sql.connect(dbConfig);
    let result = await pool.request().query('SELECT * FROM dbo.Vehiculos');
    res.status(200).json(result.recordset);
  } catch (err) {
    res.status(500).send({ mensaje: 'Error al obtener los vehículos', error: err });
  }
});

app.post('/vehiculos', async (req, res) => {
  const { modelo, marca, linea } = req.body;
  if (!modelo || !marca || !linea) {
    return res.status(400).json({ mensaje: 'modelo, marca y linea son campos requeridos.' });
  }
  try {
    let pool = await sql.connect(dbConfig);
    let result = await pool.request()
      .input('modelo', sql.NVarChar, modelo)
      .input('marca', sql.NVarChar, marca)
      .input('linea', sql.NVarChar, linea)
      .query('INSERT INTO dbo.Vehiculos (modelo, marca, linea) VALUES (@modelo, @marca, @linea); SELECT SCOPE_IDENTITY() AS id;');
    res.status(201).json({ id: result.recordset[0].id, modelo, marca, linea });
  } catch (err) {
    res.status(500).send({ mensaje: 'Error al guardar el vehículo', error: err });
  }
});

// =================== CARTELERA ===================

/**
 * @swagger
 * /cartelera3562:
 *   get:
 *     summary: Retorna una lista de todas las funciones en cartelera
 *     tags: [Cartelera]
 *     responses:
 *       '200':
 *         description: Lista de funciones obtenida exitosamente
 *   post:
 *     summary: Crea una nueva función en la cartelera
 *     tags: [Cartelera]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             example:
 *               titulo: "Avengers: Endgame"
 *               descripcion: "Película de superhéroes de Marvel"
 *               fecha: "2025-09-30"
 *               hora: "18:30"
 *               sala: "Sala 1"
 *     responses:
 *       '201':
 *         description: Función creada exitosamente
 */
app.get('/cartelera3562', async (req, res) => {
  try {
    let pool = await sql.connect(dbConfig);
    let result = await pool.request().query('SELECT * FROM dbo.cartelera3562');
    res.status(200).json(result.recordset);
  } catch (err) {
    res.status(500).send({ mensaje: 'Error al obtener la cartelera', error: err });
  }
});

app.post('/cartelera3562', async (req, res) => {
  const { titulo, descripcion, fecha, hora, sala } = req.body;
  if (!titulo || !fecha || !hora || !sala) {
    return res.status(400).json({ mensaje: 'titulo, fecha, hora y sala son campos requeridos.' });
  }
  try {
    let pool = await sql.connect(dbConfig);
    let result = await pool.request()
      .input('titulo', sql.NVarChar, titulo)
      .input('descripcion', sql.NVarChar, descripcion)
      .input('fecha', sql.Date, fecha)
      .input('hora', sql.NVarChar, hora)
      .input('sala', sql.NVarChar, sala)
      .query('INSERT INTO dbo.cartelera3562 (titulo, descripcion, fecha, hora, sala) VALUES (@titulo, @descripcion, @fecha, @hora, @sala); SELECT SCOPE_IDENTITY() AS id;');
    res.status(201).json({ id: result.recordset[0].id, titulo, descripcion, fecha, hora, sala });
  } catch (err) {
    res.status(500).send({ mensaje: 'Error al guardar en la cartelera', error: err });
  }
});

// =================== SERVIDOR ===================

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
  console.log(`Documentación de Swagger disponible en http://localhost:${PORT}/api-docs`);
});