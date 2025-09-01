import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../components/RH/Dashboard.vue'
import Acceuil from '../components/RH/Acceuil.vue'
import Candidat from '@/components/CANDIDAT/Candidat.vue';

const routes = [
  { path: '/', name : 'Dashboard',component: Dashboard },
  {path:'/acceuil', name: 'Acceuil', component:Acceuil},
  {path:'/candidat', name: 'Candidat', component:Candidat},
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
