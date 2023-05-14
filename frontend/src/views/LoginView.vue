<script setup>
import AuthComponent from "../components/AuthComponent.vue";
</script>

<template>
    <AuthComponent title="Вход">
        <form id="form" @submit="onSubmit">
            <input class="card-item" name="login"  type="text" v-model="loginForm.login" required placeholder="Email">
            <input class="card-item" name="password" type="text" v-model="loginForm.password" required placeholder="Пароль">
            <button class="card-item">Войти</button>
        </form>
        <p>{{ message }}</p>
    </AuthComponent>
</template>

<script>
    import axios from "axios";

    export default {
        data() {
            return {
                loginForm: {
                    login: '',
                    password: '',
                },
                message: ''
            }
        },
        methods: {
            login(user){
                new Promise ((resolve, reject) => {
                    axios.post("http://localhost:5000/auth/login", user)
                        .then(resp => {
                            const token = resp.data.data.token
                            localStorage.setItem('user-token', token) // store the token in localstorage

                            window.dispatchEvent(new CustomEvent('foo-key-localstorage-changed', {
                                detail: {
                                    storage: localStorage.getItem('user-token')
                                }
                            }));

                            resolve(resp)
                        })
                        .catch((error) => {
                            this.message = error.response.data.error;
                            localStorage.removeItem('user-token') // if the request fails, remove any possible user token if possible
                            reject(error)
                        });
                }).then(() => {
                    this.$router.push('/');
                })
            },
            initForm() {
                this.loginForm.login = '';
                this.loginForm.password = '';
            },
            onSubmit(evt) {
                evt.preventDefault();
                const payload = {
                    email: this.loginForm.login,
                    password: this.loginForm.password,
                };
                this.login(payload);
                this.initForm();
            },
        }
    }
</script>

<style scoped>
form
{
    display: grid;
}

.card-item
{
    margin: 5px 0;
}

button
{
    background-color: var(--vt-c-green-lighter);
    color: var(--vt-c-black);
    border: 1px solid var(--vt-c-divider-dark-1);
    border-radius: 4px;
    transition: 0.4s;
}

@media (hover: hover) {
    button:hover {
        background-color: hsla(160, 100%, 37%, 0.4);
    }
}
</style>