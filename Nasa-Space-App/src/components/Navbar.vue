<script setup>
import { RouterLink } from 'vue-router';
import router from '@/router';

</script>

<template>
  <div class="navbar navbar-expand-lg navbar-dark sticky-top bg-primary">
    <div class="container">
      <div class="align-items-center navbar-nav">
        <RouterLink class="navbar-brand" :to="{ name: 'home' }">
          <img             
            class="d-inline-block rounded-circle"
            src="../assets/nasalogo.png"
            alt="CPCDQ"
            width="60">
          Accueil
        </RouterLink>
      </div>
    </div>
  </div>
</template>
