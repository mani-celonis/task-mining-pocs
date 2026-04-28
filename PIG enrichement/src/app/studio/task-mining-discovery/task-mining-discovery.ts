import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import {
  CeButtonModule,
  CeInfoModule,
  CeMainContentModule,
  CeKpiModule,
  CePanelModule,
} from '@celonis/emotion';

@Component({
  selector: 'app-task-mining-discovery',
  imports: [
    RouterLink,
    CeMainContentModule,
    CeKpiModule,
    CePanelModule,
    CeButtonModule,
    CeInfoModule,
  ],
  templateUrl: './task-mining-discovery.html',
  styleUrl: './task-mining-discovery.scss',
})
export class TaskMiningDiscoveryPage {
  protected readonly taskMiningSteps = [
    'Receive Order Email',
    'Open Order Attachment',
    'Copy Customer ID',
    'Navigate to ERP Screen',
    'Paste Customer ID',
    'Key in Order Units',
    'Perform Price Lookup',
  ] as const;

  protected readonly salesOrderSteps = [
    'Create Sales Order',
    'Create Sales Order Item',
    'Approve Sales Order',
    'Confirm Sales Order',
    'Record Goods Receipt',
    'Create Delivery',
    'Post Goods Issue',
  ] as const;

  /** Index in taskMiningSteps that links to sales order lane */
  protected readonly bridgeTaskIndex = 6;
  protected readonly bridgeOrderIndex = 1;
}
