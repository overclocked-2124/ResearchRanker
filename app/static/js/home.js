
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import{getAuth, onAuthStateChanged, signOut} from "https://www.gstatic.com/firebasejs/11.2.0/firebase-auth.js"
import{getFirestore, getDoc, doc} from  "https://www.gstatic.com/firebasejs/11.2.0/firebase-firestore.js"
 // Your web app's Firebase configuration
 const firebaseConfig = {
   apiKey: "AIzaSyA9v6b24QAj0wCvy7h_AxeW_LaHLFy4K0A",
   authDomain: "researchranker-ae250.firebaseapp.com",
   projectId: "researchranker-ae250",
   storageBucket: "researchranker-ae250.firebasestorage.app",
   messagingSenderId: "842803859783",
   appId: "1:842803859783:web:1c20cf5671c2b7b2d73c62",
   measurementId: "G-7SH6FYE2ZQ"
 };
 
const app = initializeApp(firebaseConfig);
const auth=getAuth();
const db =getFirestore();
const logOutButton = document.getElementById("Logout");
document.getElementById("nametag").style.display='none';


onAuthStateChanged(auth,(User)=>{
    const loggedInUserId=localStorage.getItem('loggedInUserId');
    if(loggedInUserId){
        const docRef = doc(db,"users",loggedInUserId);
        getDoc(docRef)
        .then((docSnap)=>{
            if(docSnap.exists()){
                const userData = docSnap.data()
                document.getElementById("nametag").style.display='block';
            document.getElementById("nametag").innerText=userData.name;
            document.getElementById('Login').style.display='none';
            }
            else{}
        })
    }
})
logOutButton.addEventListener('click',(event)=>{
  event.preventDefault();
  
})