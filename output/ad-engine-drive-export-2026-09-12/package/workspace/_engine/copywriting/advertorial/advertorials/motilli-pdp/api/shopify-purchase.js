import crypto from 'crypto';

const PIXEL_ID = '2820311848306259';
const ACCESS_TOKEN = '[REDACTED_SECRET]';
const API_VERSION = 'v21.0';
const SHOPIFY_WEBHOOK_SECRET = process.env.SHOPIFY_WEBHOOK_SECRET || '';

function verifyShopifyWebhook(rawBody, hmacHeader) {
    if (!SHOPIFY_WEBHOOK_SECRET) return true; // Skip verification if no secret configured
    const hash = crypto.createHmac('sha256', SHOPIFY_WEBHOOK_SECRET)
        .update(rawBody, 'utf8')
        .digest('base64');
    return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(hmacHeader || ''));
}

function hashSHA256(value) {
    if (!value) return undefined;
    return crypto.createHash('sha256').update(value.trim().toLowerCase()).digest('hex');
}

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        // Verify Shopify webhook signature if secret is set
        const hmac = req.headers['x-shopify-hmac-sha256'];
        if (SHOPIFY_WEBHOOK_SECRET && hmac) {
            const rawBody = JSON.stringify(req.body);
            try {
                if (!verifyShopifyWebhook(rawBody, hmac)) {
                    return res.status(401).json({ error: 'Invalid signature' });
                }
            } catch (e) {
                return res.status(401).json({ error: 'Signature verification failed' });
            }
        }

        const order = req.body;

        // Extract order data
        const orderValue = parseFloat(order.total_price) || 0;
        const currency = (order.currency || 'USD').toUpperCase();
        const orderId = order.id || order.order_number || '';
        const email = order.email || order.contact_email || '';
        const phone = order.phone || (order.billing_address && order.billing_address.phone) || '';
        const firstName = (order.customer && order.customer.first_name) || (order.billing_address && order.billing_address.first_name) || '';
        const lastName = (order.customer && order.customer.last_name) || (order.billing_address && order.billing_address.last_name) || '';
        const city = (order.billing_address && order.billing_address.city) || '';
        const state = (order.billing_address && order.billing_address.province_code) || '';
        const zip = (order.billing_address && order.billing_address.zip) || '';
        const country = (order.billing_address && order.billing_address.country_code) || '';

        // Build content_ids from line items
        const contentIds = (order.line_items || []).map(item =>
            item.variant_id ? String(item.variant_id) : String(item.product_id)
        );
        const numItems = (order.line_items || []).reduce((sum, item) => sum + (item.quantity || 1), 0);

        // Build user_data with hashed PII for matching
        const userData = {
            client_ip_address: req.headers['x-forwarded-for'] || req.headers['x-real-ip'] || '',
            client_user_agent: req.headers['user-agent'] || ''
        };
        if (email) userData.em = [hashSHA256(email)];
        if (phone) userData.ph = [hashSHA256(phone.replace(/\D/g, ''))];
        if (firstName) userData.fn = [hashSHA256(firstName)];
        if (lastName) userData.ln = [hashSHA256(lastName)];
        if (city) userData.ct = [hashSHA256(city)];
        if (state) userData.st = [hashSHA256(state)];
        if (zip) userData.zp = [hashSHA256(zip)];
        if (country) userData.country = [hashSHA256(country)];

        // Check for fbc/fbp in order note attributes or landing_site URL params
        const noteAttrs = order.note_attributes || [];
        const fbcAttr = noteAttrs.find(a => a.name === '_fbc');
        const fbpAttr = noteAttrs.find(a => a.name === '_fbp');
        if (fbcAttr && fbcAttr.value) userData.fbc = fbcAttr.value;
        if (fbpAttr && fbpAttr.value) userData.fbp = fbpAttr.value;

        // Also check landing_site for fbclid
        if (!userData.fbc && order.landing_site) {
            const match = order.landing_site.match(/fbclid=([^&]+)/);
            if (match) {
                userData.fbc = 'fb.1.' + Date.now() + '.' + match[1];
            }
        }

        const eventId = 'purchase_' + orderId + '_' + Date.now();

        const payload = {
            data: [
                {
                    event_name: 'Purchase',
                    event_id: eventId,
                    event_time: Math.floor(Date.now() / 1000),
                    event_source_url: 'https://shop.trymotilli.co',
                    action_source: 'website',
                    user_data: userData,
                    custom_data: {
                        content_name: 'Motilli Celery Juice Gummies',
                        content_ids: contentIds.length > 0 ? contentIds : ['44383580749926'],
                        content_type: 'product',
                        value: orderValue,
                        currency: currency,
                        num_items: numItems,
                        order_id: String(orderId)
                    }
                }
            ]
        };

        const url = `https://graph.facebook.com/${API_VERSION}/${PIXEL_ID}/events?access_token=[REDACTED_SECRET]

        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            console.error('Meta CAPI Purchase error:', JSON.stringify(result));
            return res.status(response.status).json(result);
        }

        console.log('Purchase event sent for order', orderId, '- value:', orderValue, currency);
        return res.status(200).json({ success: true, events_received: result.events_received, order_id: orderId });
    } catch (err) {
        console.error('Purchase webhook error:', err.message);
        return res.status(500).json({ error: 'Internal server error' });
    }
}
