import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {
  CeMainContentModule,
  CeMainLayoutModule,
  CeMainSideNavLinkModule,
  CeMainSideNavModule,
} from '@celonis/emotion';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    CeMainLayoutModule,
    CeMainContentModule,
    CeMainSideNavModule,
    CeMainSideNavLinkModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {}
