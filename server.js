import express from 'express';
import axios from 'axios';

const app = express();
const port = 8000;

app.get('/', (req, res) => {
    console.log("this worked")
  });

app.get('/callback', async (req, res) => {
    console.log("I'm here");
    const code = req.query.code;
    const authOptions = {
        url: 'https://accounts.spotify.com/api/token',
        headers: {
            'Authorization': `Basic ${Buffer.from(`${client_id}:${client_secret}`).toString('base64')}`,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        params: {
            grant_type: 'authorization_code',
            code: code,
            redirect_uri: `http://localhost:${port}/callback`,
        },
    };

    try {
    const response = await axios.post(authOptions.url, null, { params: authOptions.params, headers: authOptions.headers });
    const access_token = response.data.access_token;

    // Use access token to make authorized API requests
    const userResponse = await axios.get('https://api.spotify.com/v1/me', {
        headers: {
        'Authorization': `Bearer ${access_token}`,
        },
    });

    // You can handle user data here
    const userData = userResponse.data;

    // Print user data to console
    console.log(userData);

    // Send user data back to the client
    res.json(userData);

    } catch (error) {
    console.error('Error exchanging code for access token:', error.message);
    res.status(500).send('Internal server error');
    }

    // Note: You can remove this line since the response is already sent
    // res.send('Authorization code exchanged successfully!');
    });

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});