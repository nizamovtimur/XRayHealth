<script setup>
    defineProps(['title'])
</script>

<template>
    <div class="container">
        <h1>{{ title }}</h1>
        <div class="card">
            <slot></slot>
        </div>
    </div>
</template>

<style scoped>
  .container
  {
      margin: 208px 0;
      display: grid;
      align-content: center;
      justify-content: center;
  }
  .card
  {
      padding: 30px 10px;
      display: grid;
      border: 1px solid var(--vt-c-divider-light-2);
  }
  h1
  {
      text-align: center;
      margin-bottom: 20px;
      color: var(--vt-c-black-soft);
  }
</style>