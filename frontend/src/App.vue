
<template>
  <div>
    <h1>Mon projet Vue-Django</h1>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: ''
    }
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:8000/dollo/hello');
      this.message = response.data.message;
    } catch (error) {
      this.message = 'Erreur de connexion au backend';
    }
  }
}
</script>
