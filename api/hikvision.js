export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end();
  }

  let body = '';
  req.on('data', chunk => {
    body += chunk.toString();
  });

  req.on('end', () => {
    console.log('HIKVISION RAW DATA:', body);

    // hozircha faqat qabul qilamiz
    // keyin:
    // 1) parse
    // 2) DB
    // 3) Telegram

    res.status(200).send('OK');
  });
}
