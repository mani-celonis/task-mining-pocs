import {
  ApplicationConfig,
  importProvidersFrom,
  provideBrowserGlobalErrorListeners,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import {
  TranslateModule,
  TranslateLoader,
  TranslationObject,
} from '@ngx-translate/core';
import { Observable, of } from 'rxjs';

import { routes } from './app.routes';
import emotionTranslations from '@celonis/emotion/assets/i18n/emotion/en.translations.bundle.json';

type EmotionTranslationsBundle = {
  emotion: Record<string, string>;
};

function unflatten(obj: Record<string, string>): TranslationObject {
  const result: TranslationObject = {};
  for (const [key, value] of Object.entries(obj)) {
    const parts = key.split('.');
    let current: TranslationObject = result;
    for (let i = 0; i < parts.length - 1; i++) {
      current[parts[i]] ??= {};
      current = current[parts[i]] as TranslationObject;
    }
    current[parts[parts.length - 1]] = value;
  }
  return result;
}

class EmotionTranslateLoader extends TranslateLoader {
  getTranslation(_lang: string): Observable<TranslationObject> {
    const bundle = emotionTranslations as EmotionTranslationsBundle;
    return of({ emotion: unflatten(bundle.emotion) });
  }
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideAnimations(),
    importProvidersFrom(
      TranslateModule.forRoot({
        loader: { provide: TranslateLoader, useClass: EmotionTranslateLoader },
        defaultLanguage: 'en',
      }),
    ),
  ],
};
