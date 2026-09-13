import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import morgan from 'morgan';
import rateLimit from 'express-rate-limit';
import { config } from './config';
import { errorHandler } from './api/middleware/errorHandler';

// Routes
import merchantRoutes from './api/routes/merchants';
import transactionRoutes from './api/routes/transactions';
import payoutRoutes from './api/routes/payouts';
import webhookRoutes from './api/routes/webhooks';
import adminRoutes from './api/routes/admin';

const app = express();

// Security
app.use(helmet());
app.use(cors({
  origin: config.nodeEnv === 'production'
    ? ['https://dashboard.yourdomain.com']
    : '*',
}));

// Rate limiting
const apiLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 100,            // 100 requests per minute per IP
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests', code: 'rate_limited' },
});

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10,                   // 10 login attempts per 15 min
  message: { error: 'Too many login attempts', code: 'rate_limited' },
});

// Body parsing
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(compression());

// Logging
if (config.nodeEnv !== 'test') {
  app.use(morgan('short'));
}

// Trust proxy (for rate limiting behind load balancer)
app.set('trust proxy', 1);

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', version: '1.0.0', timestamp: new Date().toISOString() });
});

// API routes
const v1 = `/api/${config.apiVersion}`;

app.use(`${v1}/merchants`, apiLimiter, merchantRoutes);
app.use(`${v1}/transactions`, apiLimiter, transactionRoutes);
app.use(`${v1}/payouts`, apiLimiter, payoutRoutes);
app.use(`${v1}/webhooks`, apiLimiter, webhookRoutes);
app.use(`${v1}/admin`, adminRoutes);

// Rate limit admin login specifically
app.use(`${v1}/admin/login`, authLimiter);

// 404
app.use((_req, res) => {
  res.status(404).json({ error: 'Not found', code: 'not_found' });
});

// Error handler
app.use(errorHandler);

export default app;
