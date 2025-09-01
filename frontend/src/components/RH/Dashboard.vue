<template>
  <div class="dashboard">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-logo">RH Dashboard</div>
      <div class="nav-links">
        <div class="nav-item" :class="{active: currentTab==='offres'}" @click="currentTab='offres'">Offres d'emploi</div>
        <div class="nav-item" :class="{active: currentTab==='evaluations'}" @click="currentTab='evaluations'">Évaluations</div>
        <div class="nav-item" :class="{active: currentTab==='candidats'}" @click="currentTab='candidats'">Candidatures</div>
      </div>
    </nav>

    <!-- Message succès -->
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

    <main class="main-content">

      <!-- OFFRES -->
      <div v-if="currentTab==='offres'" class="section">
        <div class="section-header">
          <h2>Offres d'emploi</h2>
          <button class="add-btn" @click="showAddOffre = true">➕ Ajouter</button>
        </div>
        <ul>
          <li v-for="offre in offres" :key="offre.id" class="card">
            <div class="card-content">
              <strong>{{ offre.titre }}</strong>
              <p>{{ offre.description }}</p>
              <span class="date">(Publié le {{ new Date(offre.date_publication).toLocaleDateString() }})</span>
            </div>
            <div class="card-actions">
              <button class="add-btn" @click="ouvrirModifierOffre(offre)">Modifier</button>
              <button class="cv-btn" @click="supprimerOffre(offre.id)">Supprimer</button>
            </div>
          </li>
        </ul>
      </div>

      <!-- ÉVALUATIONS -->
      <div v-if="currentTab==='evaluations'" class="section">
        <div class="section-header">
          <h2>Évaluations</h2>
          <button class="add-btn" @click="showAddEvaluation = true">➕ Ajouter</button>
        </div>
        <ul>
          <li v-for="evaluation in evaluations" :key="evaluation.id" class="card">
            <div class="card-content">
              <strong>{{ evaluation.titre }}</strong>
              <p>Note: {{ evaluation.note }}/10 - Évaluateur: {{ evaluation.evaluateur }}</p>
              <p>Offre liée: {{ evaluation.offre_titre }}</p>

              <!-- Liste candidats associés à l'évaluation -->
              <ul>
                <li v-for="candidat in evaluation.candidats" :key="candidat.id" class="card-candidat">
                  <div class="profile-pic" :style="{ backgroundImage: 'url(' + (candidat.photo_url ? `http://127.0.0.1:8000/dollo${candidat.photo_url}` : defaultPhoto) + ')' }"></div>
                  <div class="card-info">
                    <strong>{{ candidat.nom }} {{ candidat.prenom }}</strong>
                    <p>Email: {{ candidat.email }}</p>
                    <p>
                      {{ candidat.telephone ? 'Tel: ' + candidat.telephone : '' }}
                      {{ candidat.adresse ? '| ' + candidat.adresse : '' }}
                    </p>
                  </div>
                  <div>
                    <button class="cv-btn" @click="showCV(candidat.cv_url)">📄 CV</button>
                  </div>
                </li>
              </ul>

              <!-- Bouton mail unique pour tous les candidats de l'évaluation -->
              <div style="margin-top:10px;">
                <button class="add-btn" @click="sendMail(evaluation)">📧 Envoyer mail à tous les candidats</button>
                <button class="add-btn" @click="startJitsiMeeting(evaluation.jitsi_link)">🚀 Rejoindre la réunion</button>
              </div>
            </div>
            <div class="card-actions">
              <button class="add-btn" @click="ouvrirModifierEvaluation(evaluation)">Modifier</button>
              <button class="cv-btn" @click="supprimerEvaluation(evaluation.id)">Supprimer</button>
            </div>
          </li>
        </ul>
      </div>

      <!-- CANDIDATURES -->
      <div v-if="currentTab==='candidats'" class="section" style="display:flex; gap:20px;">
        <div class="candidats-filtres">
          <h3>Filtrer les candidatures</h3>
          <label>Date début :</label>
          <input type="date" v-model="dateDebut"/>
          <label>Date fin :</label>
          <input type="date" v-model="dateFin"/>
          <label>Emploi :</label>
          <select v-model="emploiFiltre">
            <option value="">Tous</option>
            <option v-for="offre in offres" :key="offre.id" :value="offre.titre">{{ offre.titre }}</option>
          </select>
          <button @click="filtrerCandidats" class="filter-btn">Analyser</button>
        </div>

        <div class="candidats-list">
          <ul>
            <li v-for="candidat in candidatsFiltres" :key="candidat.id" class="card card-candidat">
              <div class="profile-pic" :style="{ backgroundImage: 'url(' + (candidat.photo_url ? `http://127.0.0.1:8000/dollo${candidat.photo_url}` : defaultPhoto) + ')' }"></div>
              <div class="card-info">
                <strong>{{ candidat.nom }} {{ candidat.prenom }}</strong>
                <p>Email: {{ candidat.email }}</p>
                <p>
                  {{ candidat.telephone ? 'Tel: ' + candidat.telephone : '' }}
                  {{ candidat.adresse ? '| ' + candidat.adresse : '' }}
                </p>
              </div>
              <div>
                <button class="cv-btn" @click="showCV(candidat.cv_url)">📄 CV</button>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <p v-if="!offres.length && !evaluations.length && !candidats.length" class="default-msg">
        Cliquez sur une section pour afficher les données.
      </p>

      <!-- MODALS AJOUT / MODIFIER OFFRE -->
      <div v-if="showAddOffre || showModifierOffre" class="modal" @click.self="closeOffreModal">
        <div class="modal-content">
          <h3>{{ showModifierOffre ? 'Modifier Offre' : 'Ajouter Offre' }}</h3>
          <input v-model="newOffre.titre" placeholder="Titre"/>
          <textarea v-model="newOffre.description" placeholder="Description"></textarea>
          <input type="date" v-model="newOffre.date_fin"/>
          <div style="display:flex; justify-content:space-between;">
            <button @click="showModifierOffre ? modifierOffre() : ajouterOffre()">
              {{ showModifierOffre ? 'Modifier' : 'Ajouter' }}
            </button>
            <button @click="closeOffreModal">Annuler</button>
          </div>
        </div>
      </div>

      <!-- MODALS AJOUT / MODIFIER ÉVALUATION -->
      <div v-if="showAddEvaluation || showModifierEvaluation" class="modal" @click.self="closeEvaluationModal">
        <div class="modal-content">
          <h3>{{ showModifierEvaluation ? 'Modifier Évaluation' : 'Ajouter Évaluation' }}</h3>
          <input v-model="newEvaluation.titre" placeholder="Titre"/>
          <input type="number" v-model="newEvaluation.note" placeholder="Note"/>
          <input v-model="newEvaluation.evaluateur" placeholder="Évaluateur"/>
          <input type="datetime-local" v-model="newEvaluation.date_evaluation"/>
          <select v-model="newEvaluation.offre">
            <option value="">Sélectionner l'offre</option>
            <option v-for="offre in offres" :key="offre.id" :value="offre.id">{{ offre.titre }}</option>
          </select>
          <div style="display:flex; justify-content:space-between; margin-top:10px;">
            <button @click="showModifierEvaluation ? modifierEvaluation() : ajouterEvaluation()">
              {{ showModifierEvaluation ? 'Modifier' : 'Ajouter' }}
            </button>
            <button @click="closeEvaluationModal">Annuler</button>
          </div>
        </div>
      </div>

      <!-- MODAL CV -->
      <transition name="fade">
        <div v-if="showCVModal" class="modal" @click.self="closeCV">
          <div class="modal-content" style="width:80%; max-width:800px;">
            <iframe :src="cvModalUrl" width="100%" height="500px"></iframe>
            <button @click="closeCV" class="cancel-btn" style="margin-top:10px;">Fermer</button>
          </div>
        </div>
      </transition>

      <!-- Modal pour la visioconférence -->
<div v-if="showJitsiModal" class="modal" @click.self="closeJitsi">
  <div class="modal-content" style="width:80%; max-width:900px; height:600px;">
    <div id="jitsi-container" style="width:100%; height:100%;"></div>
    <button @click="closeJitsi" class="cancel-btn" style="margin-top:10px;">Fermer</button>
  </div>
</div>

    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      currentTab: 'offres',
      offres: [],
      evaluations: [],
      candidats: [],
      candidatsFiltres: [],
      defaultPhoto: 'https://via.placeholder.com/60',
      successMessage: '',
      dateDebut: '',
      dateFin: '',
      emploiFiltre: '',
      showAddOffre: false,
      showModifierOffre: false,
      newOffre: { id:null, titre:'', description:'', date_fin:'' },
      showAddEvaluation: false,
      showModifierEvaluation: false,
      newEvaluation: { id:null, titre:'', note:0, evaluateur:'', offre:null, date_evaluation:'' },
      showCVModal: false,
      cvModalUrl: null,
      showJitsiModal: false,
      jitsiApi: null,
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      try {
        const [offresRes, evalRes, candRes] = await Promise.all([
          axios.get("http://127.0.0.1:8000/dollo/api/offres/"),
          axios.get("http://127.0.0.1:8000/dollo/api/evaluations/"),
          axios.get("http://127.0.0.1:8000/dollo/api/candidatures/")
        ]);

        this.offres = offresRes.data;
        this.candidats = candRes.data;
        this.candidatsFiltres = [...this.candidats];

        this.evaluations = evalRes.data.map(e => {
          const candidatsEval = this.candidats.filter(c => c.offre === e.offre);
          return {...e, offre_titre: this.offres.find(o => o.id === e.offre)?.titre || 'Non liée', candidats: candidatsEval};
        });

      } catch(e) {
        alert("Erreur lors du chargement des données.");
        console.error(e);
      }
    },

    filtrerCandidats() {
      this.candidatsFiltres = this.candidats.filter(c => {
        let ok = true;
        if(this.dateDebut) ok = ok && new Date(c.date_naissance) >= new Date(this.dateDebut);
        if(this.dateFin) ok = ok && new Date(c.date_naissance) <= new Date(this.dateFin);
        if(this.emploiFiltre) ok = ok && c.offre_titre === this.emploiFiltre;
        return ok;
      });
    },

    // --- OFFRES ---
    async ajouterOffre() {
      try {
        await axios.post("http://127.0.0.1:8000/dollo/api/offres/ajout/", this.newOffre);
        this.successMessage = "Offre ajoutée ✅";
        this.closeOffreModal();
        this.loadData();
        setTimeout(() => this.successMessage='', 3000);
      } catch(e) { alert("Erreur lors de l'ajout de l'offre."); console.error(e); }
    },
    ouvrirModifierOffre(offre) { this.showModifierOffre = true; this.newOffre = { ...offre }; },
    closeOffreModal() { this.showAddOffre = false; this.showModifierOffre = false; this.newOffre = { id:null, titre:'', description:'', date_fin:'' }; },
    async modifierOffre() {
      try {
        await axios.put(`http://127.0.0.1:8000/dollo/api/offres/${this.newOffre.id}/modifier/`, this.newOffre);
        this.successMessage = "Offre modifiée ✅";
        this.closeOffreModal();
        this.loadData();
        setTimeout(() => this.successMessage='', 3000);
      } catch(e) { alert("Erreur lors de la modification de l'offre."); console.error(e); }
    },
    async supprimerOffre(id) {
      if(confirm("Voulez-vous vraiment supprimer cette offre ?")) {
        try {
          await axios.delete(`http://127.0.0.1:8000/dollo/api/offres/${id}/supprimer/`);
          this.successMessage = "Offre supprimée ✅";
          this.loadData();
          setTimeout(() => this.successMessage='', 3000);
        } catch(e) { alert("Erreur lors de la suppression de l'offre."); console.error(e); }
      }
    },

    // --- ÉVALUATIONS ---
    async ajouterEvaluation() {
      try {
        if(!this.newEvaluation.offre) {
          alert("Veuillez sélectionner une offre pour l'évaluation.");
          return;
        }
        const payload = {
          titre: this.newEvaluation.titre,
          note: this.newEvaluation.note,
          evaluateur: this.newEvaluation.evaluateur,
          offre: this.newEvaluation.offre,
          date_evaluation: this.newEvaluation.date_evaluation
        };
        const response = await axios.post("http://127.0.0.1:8000/dollo/api/evaluations/ajout/", payload);
        this.successMessage = response.data.message || "Évaluation ajoutée ✅";
        this.closeEvaluationModal();
        this.loadData();
        setTimeout(() => this.successMessage='', 3000);
      } catch(e) {
        alert("Erreur lors de l'ajout de l'évaluation.");
        console.error(e);
      }
    },
    ouvrirModifierEvaluation(evaluation) { this.showModifierEvaluation = true; this.newEvaluation = { ...evaluation, offre: evaluation.offre }; },
    closeEvaluationModal() { this.showAddEvaluation = false; this.showModifierEvaluation = false; this.newEvaluation = { id:null, titre:'', note:0, evaluateur:'', offre:null, date_evaluation:'' }; },
    async modifierEvaluation() {
      try {
        const payload = {
          titre: this.newEvaluation.titre,
          note: this.newEvaluation.note,
          evaluateur: this.newEvaluation.evaluateur,
          offre: this.newEvaluation.offre,
          date_evaluation: this.newEvaluation.date_evaluation
        };
        await axios.put(`http://127.0.0.1:8000/dollo/api/evaluations/${this.newEvaluation.id}/modifier/`, payload);
        this.successMessage = "Évaluation modifiée ✅";
        this.closeEvaluationModal();
        this.loadData();
        setTimeout(() => this.successMessage='', 3000);
      } catch(e) { alert("Erreur lors de la modification de l'évaluation."); console.error(e); }
    },
    async supprimerEvaluation(id) {
      if(confirm("Voulez-vous vraiment supprimer cette évaluation ?")) {
        try {
          await axios.delete(`http://127.0.0.1:8000/dollo/api/evaluations/${id}/supprimer/`);
          this.successMessage = "Évaluation supprimée ✅";
          this.loadData();
          setTimeout(() => this.successMessage='', 3000);
        } catch(e) { alert("Erreur lors de la suppression de l'évaluation."); console.error(e); }
      }
    },

    // --- CV ---
    showCV(filename) {
      if(filename) {
        this.cvModalUrl = `http://127.0.0.1:8000/dollo${filename}`;
        this.showCVModal = true;
      } else {
        alert("Pas de CV disponible pour ce candidat.");
      }
    },
    closeCV() { this.cvModalUrl = null; this.showCVModal = false; },

    // --- ENVOI MAIL ÉVALUATION ---
    // --- ENVOI MAIL ÉVALUATION ---
async sendMail(evaluation) {
  try {
    // L'ID de l'évaluation est passé dans l'URL
    const response = await axios.post(`http://127.0.0.1:8000/dollo/api/evaluations/${evaluation.id}/send_email/`, {
      // Tu peux envoyer d'autres infos si nécessaire, par ex. date, heure, lien
      date: evaluation.date_evaluation?.split("T")[0] || "",
      time: evaluation.date_evaluation?.split("T")[1] || "",
      link: "https://lien-vers-la-reunion.com"
    });
    this.successMessage = response.data.message || "Emails envoyés ✅";
    setTimeout(() => this.successMessage = '', 3000);
  } catch(e) {
    alert("Erreur lors de l'envoi des mails.");
    console.error(e);
  }
},


async startJitsiMeeting(link) {
  try {
    this.showJitsiModal = true;

    // 1. Vérifie et demande l'accès au micro et à la caméra
    await navigator.mediaDevices.getUserMedia({ video: true, audio: true });

    this.$nextTick(() => {
      const container = document.getElementById("jitsi-container");
      if (!container) {
        alert("Impossible de trouver le container Jitsi !");
        return;
      }

      // 2. Supprime l'instance précédente si existante
      if (this.jitsiApi) {
        this.jitsiApi.dispose();
        this.jitsiApi = null;
      }

      // 3. Prépare le nom de la salle à partir du lien
      const roomName = link.replace(/\/$/, '').split("/").pop();
      const domain = "meet.jit.si";

      // 4. Configure l'API Jitsi
      const options = {
        roomName: roomName,
        parentNode: container,
        width: "100%",
        height: "100%",
        configOverwrite: {
          startWithAudioMuted: false,
          startWithVideoMuted: false,
        },
        interfaceConfigOverwrite: {
          SHOW_JITSI_WATERMARK: false,
          SHOW_WATERMARK_FOR_GUESTS: false,
        },
      };

      // 5. Lance la réunion
      this.jitsiApi = new JitsiMeetExternalAPI(domain, options);
    });
  } catch (error) {
    // 6. Gère les erreurs de permissions ou autres problèmes
    console.error("Erreur lors de l'accès au micro/caméra :", error);
    alert(
      "Impossible d'accéder à votre caméra ou micro. " +
      "Vérifiez vos permissions dans le navigateur."
    );
  }
},



  closeJitsi() {
    if (this.jitsiApi) {
      this.jitsiApi.dispose();
      this.jitsiApi = null;
    }
    this.showJitsiModal = false;
  }

  }
};
</script>




<style scoped>
/* --- Styles conservés exactement comme ton dashboard actuel --- */
body{font-family:'Segoe UI', Tahoma, Geneva, Verdana,sans-serif;background:#eef6f6;margin:0;}
.navbar{display:flex;justify-content:space-between;align-items:center;background:#055A60;color:white;padding:15px 25px;box-shadow:0 4px 10px rgba(0,0,0,0.15);border-radius:0 0 15px 15px;}
.nav-logo{font-size:1.3rem;font-weight:bold;}
.nav-links{display:flex;gap:25px;}
.nav-item{padding:8px 16px;border-radius:8px;cursor:pointer;transition:all 0.3s;}
.nav-item:hover{background:rgba(255,255,255,0.2);transform:scale(1.05);}
.nav-item.active{background:white;color:#055A60;}
.success-message{position:fixed;top:60px;right:20px;background:#27ae60;color:white;padding:12px 20px;border-radius:8px;font-weight:bold;box-shadow:0 2px 6px rgba(0,0,0,0.2);animation:fade-in-out 3s forwards;}
@keyframes fade-in-out{0%{opacity:0;transform:translateY(-10px);}10%{opacity:1;transform:translateY(0);}90%{opacity:1;}100%{opacity:0;transform:translateY(-10px);}}

/* Section */
.main-content{padding:25px;}
.section{background:white;padding:25px;margin-bottom:25px;border-radius:15px;box-shadow:0 6px 15px rgba(0,0,0,0.1);transition:transform 0.2s;}
.section:hover{transform:translateY(-3px);}
h2{color:#055A60;margin-bottom:20px;font-weight:700;}
.card{display:flex;justify-content:space-between;align-items:flex-start;border-radius:12px;padding:18px 25px;margin-bottom:15px;background:#f9f9f9;box-shadow:0 4px 10px rgba(0,0,0,0.08);transition:transform 0.2s,box-shadow 0.3s;}
.card:hover{transform:translateY(-3px);box-shadow:0 6px 18px rgba(0,0,0,0.12);}
.card-info strong{font-size:1.1rem;color:#055A60;}
.card-info p{font-size:0.9rem;color:#555;margin:4px 0;}
.card-actions{display:flex;gap:10px;align-items:center;}

/* Filtres candidats */
.candidats-filtres{flex:0 0 250px;background:#055A60;padding:20px;border-radius:10px;color:white;display:flex;flex-direction:column;gap:10px;}
.candidats-filtres h3{margin-bottom:10px;font-weight:bold;}
.candidats-filtres input,.candidats-filtres select{width:100%;padding:8px;border-radius:5px;border:none;}
.filter-btn{background:#033F42;color:white;border:none;padding:10px;border-radius:6px;cursor:pointer;font-weight:bold;transition:0.3s;}
.filter-btn:hover{background:#055A60;transform:scale(1.05);}
.card-candidat{display:flex;gap:15px;padding:15px 20px;align-items:center;}
.profile-pic{width:60px;height:60px;border-radius:50%;background-size:cover;background-position:center;border:2px solid #055A60;}
.cv-btn{display:inline-block;background:#033F42;color:white;padding:8px 12px;border-radius:5px;text-decoration:none;font-weight:bold;transition:0.3s;cursor:pointer;}
.cv-btn:hover{background:#055A60;transform:scale(1.05);}
.default-msg{text-align:center;color:#555;font-style:italic;margin-top:30px;}

/* Modals */
.modal{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;justify-content:center;align-items:center;z-index:2000;}
.modal-content{background:white;padding:20px;border-radius:10px;width:400px;display:flex;flex-direction:column;gap:10px;}
.modal-content input,.modal-content textarea,.modal-content select{padding:8px;border-radius:5px;border:1px solid #ccc;}
.modal-content button{padding:8px 12px;border:none;border-radius:6px;cursor:pointer;background:#055A60;color:white;font-weight:bold;transition:0.3s;}
.modal-content button:hover{background:#033F42;}
.section-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;}
.add-btn{background:#27ae60;color:white;padding:6px 12px;border-radius:6px;border:none;cursor:pointer;font-weight:bold;transition:0.3s;}
.add-btn:hover{background:#2ecc71;}
</style>
