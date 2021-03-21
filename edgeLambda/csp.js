'use strict';
exports.handler = (event, context, callback) => {
  const response = event.Records[0].cf.response;
  const headers = response.headers;
  headers['strict-transport-security'] = [{key: 'Strict-Transport-Security', value: 'max-age=31536000'}];
  headers['content-security-policy'] = [{key: 'Content-Security-Policy', value: "default-src 'self' 'unsafe-inline' *.abs.gov.au *.arcgis.com *.openstreetmap.org unpkg.com *.gabrielsargeant.com *.googleapis.com; script-src 'self' 'unsafe-inline' 'unsafe-eval' *.abs.gov.au *.arcgis.com *.openstreetmap.org unpkg.com *.gabrielsargeant.com *.googleapis.com; object-src 'self' *.abs.gov.au *.arcgis.com *.openstreetmap.org unpkg.com *.gabrielsargeant.com *.googleapis.com; font-src 'unsafe-inline' 'self' data: *.arcgis.com ; frame-ancestors 'none'; form-action 'self'; base-uri 'none'; block-all-mixed-content;"}];
  headers['x-content-type-options'] = [{key: 'X-Content-Type-Options', value: 'nosniff'}];
  headers['X-permitted-cross-domain-policies'] = [{key: 'X-Permitted-Cross-Domain-Policies', value: 'none'}];
  headers['x-frame-options'] = [{key: 'X-Frame-Options', value: 'DENY'}];
  headers['x-xss-protection'] = [{key: 'X-XSS-Protection', value: '1; mode=block'}];
  headers['referrer-policy'] = [{key: 'Referrer-Policy', value: 'no-referrer-when-downgrade'}];
  callback(null, response);
}; 