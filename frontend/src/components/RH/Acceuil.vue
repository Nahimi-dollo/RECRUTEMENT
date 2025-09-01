<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex flex-col">
    <!-- ===== Navbar ===== -->
    <nav class="flex justify-between items-center bg-white shadow-md px-8 py-4">
      <div class="text-2xl font-bold text-blue-700">RH Recruit</div>
      <div class="space-x-6">
        <a href="#" class="text-gray-600 hover:text-blue-700 transition">Accueil</a>
        <a href="#" class="text-gray-600 hover:text-blue-700 transition">Offres</a>
        <a href="#" class="text-gray-600 hover:text-blue-700 transition">Candidats</a>
        <a href="#" class="text-gray-600 hover:text-blue-700 transition">Contact</a>
      </div>
      <button class="bg-blue-700 text-white px-4 py-2 rounded-xl shadow hover:bg-blue-800 transition">
        Connexion
      </button>
    </nav>

    <!-- ===== Hero Section ===== -->
    <section class="flex flex-col md:flex-row items-center justify-between flex-grow px-10 md:px-20 py-12">
      <!-- Texte -->
      <div class="md:w-1/2 space-y-6">
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-800 leading-tight">
          Gérez vos recrutements <span class="text-blue-700">facilement</span> et efficacement
        </h1>
        <p class="text-lg text-gray-600">
          Une plateforme complète pour publier vos offres, analyser les CV et trouver les meilleurs talents en un seul clic.
        </p>
        <div class="space-x-4">
          <button class="bg-blue-700 text-white px-6 py-3 rounded-xl shadow hover:bg-blue-800 transition">
            Découvrir
          </button>
          <button class="bg-gray-200 text-gray-800 px-6 py-3 rounded-xl hover:bg-gray-300 transition">
            En savoir plus
          </button>
        </div>
      </div>

      <!-- Image illustrée -->
      <div class="md:w-1/2 mt-10 md:mt-0">
        <img src="https://cdn.dribbble.com/users/2058955/screenshots/14396862/media/2f0e1b1fa083c5c1de87b2f6f891d5c6.png" 
             alt="Recrutement illustration" 
             class="rounded-2xl shadow-lg">
      </div>
    </section>

    <!-- ===== Footer ===== -->
    <footer class="bg-white shadow-inner py-4 text-center text-gray-500 text-sm">
      © 2025 RH Recruit. Tous droits réservés.
    </footer>
  </div>
</template>

<script>
export default {
  name: "Home",
};
</script>
