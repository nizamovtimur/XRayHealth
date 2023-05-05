<template>
  <div class="about">
    <h1>This is an about page</h1>
      <p> {{msg.data}}</p>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
      data() {
          return {
              msg: '',
          }
      },
      methods: {
          getMessage() {
              const path = "http://localhost:5000/";
              axios.get(path).then((res) => {
                  this.msg = res.data;
              })
          }
      },
      created() {
          this.getMessage();
      }
  }
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
