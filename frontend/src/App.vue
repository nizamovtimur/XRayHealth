<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <header>
        <div class="container">
            <img src="./assets/logo.svg" width="24" height="24" alt="logo">
            <nav>
                <RouterLink to="/" class="nav-item">Главная</RouterLink>
                <RouterLink v-if="!isLoggedIn" to="/register" class="nav-item">Регистрация</RouterLink>
                <RouterLink v-if="!isLoggedIn" to="/login" class="nav-item">Войти</RouterLink>
                <div v-if="isLoggedIn" class="auth-container">
                    <p class="nav-item">{{ name }}</p>
                    <a @click="logout" class="nav-item logout">Выйти</a>
                </div>
            </nav>
        </div>
    </header>

    <div class="container">
        <RouterView />
    </div>
</template>

<script>
export default
{
    mounted() {
        window.addEventListener('token-changed', (event) => {
            this.token = event.detail.storage;
            this.name = event.detail.name;
        });
        this.token = localStorage.getItem('user-token')
        this.name = localStorage.getItem('user-name')
    },
    data() {
        return {
            token: null,
            name: null
        }
    },
    computed: {
        isLoggedIn() {
            return !!this.token
        }
    },
    methods: {
        logout() {
            localStorage.removeItem('user-token')
            localStorage.removeItem('user-name')
            window.dispatchEvent(new CustomEvent('token-changed', {
                detail: {
                    storage: undefined,
                    name: undefined
                }
            }));
        }
    }
}
</script>

<style scoped>
    .container
    {
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0 auto;
        max-width: var(--vp-screen-max-width);
    }
    header
    {
        display: flex;
        border-bottom: 1px solid var(--vt-c-divider-light-2);
        padding: 0 32px;
        height: var(--vt-nav-height);
        align-items: center;
    }
    nav
    {
        display: flex;
    }
    .nav-item
    {
        padding: 12px;
    }
    .auth-container
    {
        display: flex;
    }
    .logout
    {
        cursor: pointer;
    }
</style>
