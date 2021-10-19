import i18n from "i18next";
import {initReactI18next} from "react-i18next";
import LanguageDetector from 'i18next-browser-languagedetector';

import translationFr from './fr.json';
import translationEn from './en.json';

const resources = {
    en: {translation: translationEn},
    fr: {translation: translationFr}
};

i18n.use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources,
        detection: {
            order: ['querystring', 'localStorage', 'navigator']
        },
        fallbackLng: "en",
        supportedLngs: Object.keys(resources),
        keySeparator: ".",
        initImmediate: true,
        interpolation: {
            escapeValue: false,
        }
    });

export default i18n;