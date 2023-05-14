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
        window.addEventListener('foo-key-localstorage-changed', (event) => {
            this.token = event.detail.storage;
        });
        this.token = localStorage.getItem('user-token')
    },
    data() {
        return {
            token: null,
        }
    },
    computed: {
        isLoggedIn() {
            return !!this.token
        }
    },
}
</script>

<style scoped>
    .container
    {
        width: 100%;
        display: flex;
        justify-content: space-between;
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
    .nav-item
    {
        padding: 12px;
    }
</style>
