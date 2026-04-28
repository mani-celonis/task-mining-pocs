import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    /** PiG modeling Workers view is the primary prototype surface for this branch. */
    redirectTo: '/data/pig-modeling',
  },
  {
    path: 'overview',
    loadComponent: () =>
      import('./task-mining-landing/task-mining-landing').then((m) => m.TaskMiningLanding),
  },
  {
    path: 'task-mining/analysis',
    loadComponent: () =>
      import('./task-mining-analysis/task-mining-analysis').then(
        (m) => m.TaskMiningAnalysisPage,
      ),
  },
  {
    path: 'data/pig-modeling/task-mining-project',
    loadComponent: () =>
      import('./task-mining/project/task-mining-project').then((m) => m.TaskMiningProject),
  },
  {
    path: 'task-mining/project',
    redirectTo: '/data/pig-modeling/task-mining-project',
  },
  {
    path: 'task-mining/clustering/configure',
    loadComponent: () =>
      import('./task-mining/clustering-config/clustering-config').then((m) => m.ClusteringConfigPage),
  },
  {
    path: 'task-mining/clustering/preview',
    loadComponent: () =>
      import('./task-mining/clustering-preview/clustering-preview').then(
        (m) => m.ClusteringPreviewPage,
      ),
  },
  {
    path: 'data/pig-modeling',
    loadComponent: () =>
      import('./data/pig-modeling/pig-modeling').then((m) => m.PigModelingPage),
  },
  {
    path: 'data/pig-v2',
    loadComponent: () => import('./data/pig-modeling/pig-modeling').then((m) => m.PigModelingPage),
  },
  {
    path: 'studio/process-task-mining-discovery',
    loadComponent: () =>
      import('./data/pig-modeling/pig-modeling').then((m) => m.PigModelingPage),
  },
];
