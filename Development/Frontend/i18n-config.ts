import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Translation resources
const resources = {
  en: {
    translation: {
      welcome: 'Welcome',
      login: 'Login',
      logout: 'Logout',
      register: 'Register',
      email: 'Email',
      password: 'Password',
      name: 'Name',
      submit: 'Submit',
      cancel: 'Cancel',
      save: 'Save',
      delete: 'Delete',
      edit: 'Edit',
      search: 'Search',
      loading: 'Loading...',
      error: 'An error occurred',
      success: 'Success',
      dashboard: 'Dashboard',
      profile: 'Profile',
      settings: 'Settings',
    },
  },
  es: {
    translation: {
      welcome: 'Bienvenido',
      login: 'Iniciar sesión',
      logout: 'Cerrar sesión',
      register: 'Registrarse',
      email: 'Correo electrónico',
      password: 'Contraseña',
      name: 'Nombre',
      submit: 'Enviar',
      cancel: 'Cancelar',
      save: 'Guardar',
      delete: 'Eliminar',
      edit: 'Editar',
      search: 'Buscar',
      loading: 'Cargando...',
      error: 'Ocurrió un error',
      success: 'Éxito',
      dashboard: 'Panel',
      profile: 'Perfil',
      settings: 'Configuración',
    },
  },
  fr: {
    translation: {
      welcome: 'Bienvenue',
      login: 'Connexion',
      logout: 'Déconnexion',
      register: "S'inscrire",
      email: 'Email',
      password: 'Mot de passe',
      name: 'Nom',
      submit: 'Soumettre',
      cancel: 'Annuler',
      save: 'Enregistrer',
      delete: 'Supprimer',
      edit: 'Modifier',
      search: 'Rechercher',
      loading: 'Chargement...',
      error: 'Une erreur est survenue',
      success: 'Succès',
      dashboard: 'Tableau de bord',
      profile: 'Profil',
      settings: 'Paramètres',
    },
  },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;

// Language switcher hook
export function useLanguage() {
  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  return {
    currentLanguage: i18n.language,
    changeLanguage,
    languages: Object.keys(resources),
  };
}
