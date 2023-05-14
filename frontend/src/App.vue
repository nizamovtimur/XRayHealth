<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <header>
        <div class="container">
            <img src="./assets/logo.svg" width="24" height="24" alt="logo">
            <nav>
              <RouterLink to="/" class="nav-item">Главная</RouterLink>
              <RouterLink to="/about" class="nav-item">About</RouterLink>
            </nav>
        </div>
    </header>

    <div class="container">
        <RouterView />
    </div>
</template>

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
