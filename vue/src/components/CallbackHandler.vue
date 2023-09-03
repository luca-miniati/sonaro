<template>
    <div>
      <h2>Loading...</h2>
    </div>
</template>

<script>
import axios from 'axios';
import { mapActions, mapGetters } from 'vuex';
import { Buffer } from 'buffer';

export default {
    name: 'CallbackHandler',
    async created() {
        try {
            const code = this.$route.query.code;
            const state = this.$route.query.state;

            this.$store.commit('SET_STATE', state);

            await this.getToken(code, state);

            this.$router.push('/findsongs');
        } catch (error) {
            console.error('Error processing callback:', error);
        }
    },
    methods: {
        ...mapActions(['setAccessToken', 'setRefreshToken']),
        ...mapGetters(['getState']),
        async getToken(code, state) {
            if (state != this.getState()) {
                return
            }

            const clientId = process.env.VUE_APP_CLIENT_ID;
            const clientSecret = process.env.VUE_APP_CLIENT_SECRET;

            const authOptions = {
                url: 'https://accounts.spotify.com/api/token',
                headers: {
                    'Authorization': `Basic ${(new Buffer.from(clientId + ':' + clientSecret).toString('base64'))}`,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                params: {
                    grant_type: 'authorization_code',
                    code: code,
                    redirect_uri: 'http://localhost:8000/callback',
                },
            };

            const response = await axios.post(authOptions.url, null, { params: authOptions.params, headers: authOptions.headers });

            this.setAccessToken(response.data.access_token);
            this.setRefreshToken(response.data.refresh_token);
        },
    },
};
</script>