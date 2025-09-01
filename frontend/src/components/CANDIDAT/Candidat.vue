<template>
  <div class="dashboard">
    <!-- NAVBAR -->
    <nav class="navbar">
      <div class="nav-logo">Plateforme Emploi</div>
      <div class="nav-links">
        <div class="nav-item" :class="{active: currentTab==='home'}" @click="currentTab='home'">Accueil</div>
        <div class="nav-item" :class="{active: currentTab==='offres'}" @click="currentTab='offres'">Offres d'emploi</div>
        <div class="nav-item" :class="{active: currentTab==='apropos'}" @click="currentTab='apropos'">À propos</div>
      </div>
    </nav>

    <main class="main-content">
      <!-- ACCUEIL -->
      <div v-if="currentTab==='home'" class="section home">
        <div class="home-content">
          <h1>Bienvenue sur notre plateforme d'emploi</h1>
          <p>Explorez nos offres d’emploi et trouvez le poste qui correspond à vos compétences.</p>
          <button class="add-btn" @click="currentTab='offres'">Voir les offres</button>
        </div>
        <img src="https://via.placeholder.com/900x300" alt="banner" class="banner"/>
      </div>

      <!-- OFFRES -->
      <div v-if="currentTab==='offres'" class="section">
        <h2>Nos Offres Disponibles</h2>
        <div class="jobs-list">
          <div v-for="offre in offres" :key="offre.id" class="card">
            <div class="card-content">
              <strong>{{ offre.titre }}</strong>
              <p>{{ offre.description.substring(0,120) }}...</p>
              <span class="date">(Publié le {{ new Date(offre.date_publication).toLocaleDateString() }})</span>
            </div>
            <div class="card-actions">
              <button class="add-btn" @click="ouvrirFormulaire(offre)">Postuler</button>
              <button class="add-btn" @click="toggleCandidatures(offre)">Voir Candidatures</button>
            </div>

            <!-- Liste candidatures -->
            <div v-if="offre.showCandidatures" class="candidatures-list">
              <h4>Candidatures pour {{ offre.titre }}</h4>
              <div v-if="offre.candidatures && offre.candidatures.length">
                <ul>
                  <li v-for="cand in offre.candidatures" :key="cand.id">
                    {{ cand.nom }} {{ cand.prenom }} - {{ cand.email }}
                    <button class="cv-btn" v-if="cand.cv_url" @click="afficherCV(cand)">Voir CV</button>
                  </li>
                </ul>
              </div>
              <p v-else>Aucune candidature pour le moment.</p>
            </div>

          </div>
        </div>
        <p v-if="!offres.length" class="default-msg">Aucune offre disponible pour le moment.</p>
      </div>

      <!-- A PROPOS -->
      <div v-if="currentTab==='apropos'" class="section">
        <h2>À propos</h2>
        <p>
          Cette plateforme vous connecte aux meilleures opportunités d'emploi. 
          Postulez facilement aux offres qui vous intéressent et suivez votre candidature.
        </p>
        <ul>
          <li>🔹 Plateforme simple et rapide</li>
          <li>🔹 Offres variées et mises à jour régulièrement</li>
          <li>🔹 Postulation sécurisée en ligne</li>
        </ul>
      </div>

      <!-- MODAL FORMULAIRE CANDIDATURE -->
      <transition name="fade">
        <div v-if="showCandidatureForm" class="modal" @click.self="fermerFormulaire">
          <div class="modal-content">
            <h3>Postuler à : {{ selectedOffre.titre }}</h3>

            <form @submit.prevent="submitCandidature" enctype="multipart/form-data">
              <div class="form-row">
                <div class="form-group">
                  <label>Nom</label>
                  <input type="text" v-model="candidature.nom" required placeholder="Entrez votre nom"/>
                </div>
                <div class="form-group">
                  <label>Prénom</label>
                  <input type="text" v-model="candidature.prenom" required placeholder="Entrez votre prénom"/>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Email</label>
                  <input type="email" v-model="candidature.email" required placeholder="Votre email"/>
                </div>
                <div class="form-group">
                  <label>Téléphone</label>
                  <input type="text" v-model="candidature.telephone" placeholder="Votre téléphone"/>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Adresse</label>
                  <input type="text" v-model="candidature.adresse" placeholder="Votre adresse"/>
                </div>
                <div class="form-group">
                  <label>Date de naissance</label>
                  <input type="date" v-model="candidature.date_naissance"/>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>CV</label>
                  <input type="file" @change="handleCVUpload"/>
                </div>
                <div class="form-group">
                  <label>Photo de profil</label>
                  <input type="file" @change="handlePhotoUpload"/>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group full-width">
                  <label>Offre / Poste</label>
                  <select v-model="candidature.offre" required>
                    <option :value="selectedOffre.id">{{ selectedOffre.titre }}</option>
                  </select>
                </div>
              </div>

              <div class="form-buttons">
                <button type="submit" class="submit-btn">Envoyer</button>
                <button type="button" @click="fermerFormulaire" class="cancel-btn">Annuler</button>
              </div>
            </form>

            <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
          </div>
        </div>
      </transition>

      <!-- MODAL AFFICHAGE CV -->
      <transition name="fade">
        <div v-if="showCVModal" class="modal" @click.self="showCVModal=false">
          <div class="modal-content" style="max-width:800px;">
            <h3>CV de {{ selectedCandidature.nom }} {{ selectedCandidature.prenom }}</h3>
            <iframe v-if="selectedCandidature.cv_url" :src="selectedCandidature.cv_url" style="width:100%; height:500px;" frameborder="0"></iframe>
            <p v-else>Aucun CV disponible.</p>
          </div>
        </div>
      </transition>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      currentTab: "home",
      offres: [],
      showCandidatureForm: false,
      successMessage: '',
      selectedOffre: {},
      candidature: { nom:'', prenom:'', email:'', telephone:'', adresse:'', date_naissance:'', cv:null, photo_profil:null, offre:'' },
      showCVModal: false,
      selectedCandidature: {}
    };
  },
  mounted() { this.loadOffres(); },
  methods: {
    async loadOffres() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/dollo/api/offres/");
        this.offres = res.data.map(offre => ({ ...offre, showCandidatures:false, candidatures:offre.candidatures || [] }));
      } catch(e) { alert("Erreur lors du chargement des offres."); }
    },
    ouvrirFormulaire(offre) {
      this.selectedOffre = offre;
      this.candidature.offre = offre.id;
      this.showCandidatureForm = true;
    },
    fermerFormulaire() {
      this.showCandidatureForm = false;
      this.resetForm();
    },
    handleCVUpload(event) { this.candidature.cv = event.target.files[0]; },
    handlePhotoUpload(event) { this.candidature.photo_profil = event.target.files[0]; },
    async submitCandidature() {
      const formData = new FormData();
      for (let key in this.candidature) if(this.candidature[key] !== null) formData.append(key, this.candidature[key]);
      try {
        await axios.post("http://127.0.0.1:8000/dollo/api/candidatures/ajout/", formData, { headers: { "Content-Type": "multipart/form-data" } });
        this.successMessage = "Candidature envoyée avec succès ✅";
        setTimeout(() => { this.successMessage=''; this.fermerFormulaire(); this.loadOffres(); }, 2500);
        this.resetForm();
      } catch(e) { alert("Erreur lors de l'envoi de la candidature."); console.error(e.response || e); }
    },
    resetForm() { this.candidature = { nom:'', prenom:'', email:'', telephone:'', adresse:'', date_naissance:'', cv:null, photo_profil:null, offre:'' }; },
    afficherCV(candidature) { this.selectedCandidature = candidature; this.showCVModal = true; },
    toggleCandidatures(offre) { offre.showCandidatures = !offre.showCandidatures; }
  }
};
</script>

<style scoped>
body { font-family: 'Segoe UI', sans-serif; background: #eef6f6; margin:0; }
.navbar { display:flex; justify-content:space-between; align-items:center; background: linear-gradient(90deg, #055A60, #033F42); color:white; padding:15px 25px; box-shadow:0 4px 12px rgba(0,0,0,0.2); border-radius:0 0 15px 15px; }
.nav-logo { font-size:1.4rem; font-weight:bold; }
.nav-links { display:flex; gap:25px; }
.nav-item { padding:8px 16px; border-radius:8px; cursor:pointer; transition:0.3s; }
.nav-item:hover { background: rgba(255,255,255,0.2); transform: scale(1.05);}
.nav-item.active { background:white; color:#055A60; font-weight:bold; }
.main-content { padding:30px; }
.section { background:white; padding:30px; margin-bottom:25px; border-radius:15px; box-shadow:0 8px 20px rgba(0,0,0,0.1); transition:0.3s;}
.section:hover { transform:translateY(-5px); box-shadow:0 12px 28px rgba(0,0,0,0.15); }
h1,h2 { color:#055A60; margin-bottom:20px; font-weight:700; }
.home-content { text-align:center; margin-bottom:20px; }
.banner { margin-top:20px; border-radius:12px; width:100%; box-shadow:0 6px 15px rgba(0,0,0,0.1); transition:0.3s; }
.banner:hover { transform: scale(1.02); }
.jobs-list { display:flex; flex-wrap:wrap; gap:20px; }
.card { flex:1 1 250px; background:#f9f9f9; border-radius:12px; padding:20px; box-shadow:0 6px 15px rgba(0,0,0,0.08); transition:0.3s; cursor:pointer; }
.card:hover { transform: translateY(-5px) scale(1.02); box-shadow:0 12px 28px rgba(0,0,0,0.15); }
.card-content strong { font-size:1.2rem; color:#055A60; }
.card-content p { font-size:0.95rem; color:#555; margin:8px 0; }
.card-actions { margin-top:10px; display:flex; justify-content:flex-end; gap:10px; }
.add-btn, .submit-btn, .cv-btn, .cancel-btn { border:none; border-radius:6px; padding:8px 16px; font-weight:bold; cursor:pointer; transition:0.3s; }
.add-btn { background:#27ae60; color:white; } .add-btn:hover { background:#2ecc71; transform:scale(1.1); }
.submit-btn { background:#27ae60; color:white; } .submit-btn:hover { background:#2ecc71; transform:scale(1.05); }
.cancel-btn { background:#c0392b; color:white; } .cancel-btn:hover { background:#e74c3c; transform:scale(1.05); }
.cv-btn { background:#2980b9; color:white; } .cv-btn:hover { background:#3498db; transform:scale(1.05); }
.modal { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); display:flex; justify-content:center; align-items:center; z-index:2000; }
.modal-content { background:white; padding:25px; border-radius:15px; max-width:700px; width:90%; box-shadow:0 8px 20px rgba(0,0,0,0.2); }
.form-row { display:flex; gap:20px; flex-wrap:wrap; margin-bottom:15px; }
.form-group { flex:1; display:flex; flex-direction:column; }
.form-group.full-width { flex:100%; }
.form-group label { margin-bottom:5px; font-weight:bold; }
.form-group input, .form-group select { padding:10px; border-radius:6px; border:1px solid #ccc; transition:0.3s; }
.form-group input:focus, .form-group select:focus { border-color:#27ae60; box-shadow:0 0 8px rgba(39,174,96,0.3); outline:none; }
.success-message { margin-top:15px; text-align:center; font-weight:bold; color:#27ae60; font-size:1rem; }
.default-msg { text-align:center; color:#555; font-style:italic; margin-top:30px; }
.candidatures-list { margin-top:15px; background:#f1f1f1; padding:15px; border-radius:8px; }
@media(max-width:900px){ .jobs-list{flex-direction:column;gap:15px;} .navbar{flex-direction:column;align-items:flex-start;gap:10px;} }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity:0; }
</style>
