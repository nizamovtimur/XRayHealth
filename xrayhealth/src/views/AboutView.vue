<template>
    <p> {{msg.data}}</p>
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

</style>
