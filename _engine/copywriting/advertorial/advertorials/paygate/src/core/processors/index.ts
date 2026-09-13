/**
 * Processor Registry
 *
 * Central place to initialize and access payment processors.
 * Add new processors here as you sign agreements with them.
 */

import { BaseProcessor, BaseAchProcessor } from './base';
import { NmiProcessor } from './nmi';
import { AchProcessor } from './ach';
import { config } from '../../config';
import { logger } from '../../config/logger';

class ProcessorRegistry {
  private cardProcessors: Map<string, BaseProcessor> = new Map();
  private achProcessor: BaseAchProcessor | null = null;
  private defaultCardProcessor: string = '';

  initialize() {
    // Register NMI if configured
    if (config.processors.nmi.securityKey) {
      const nmi = new NmiProcessor();
      this.cardProcessors.set(nmi.id, nmi);
      this.defaultCardProcessor = nmi.id;
      logger.info('Registered card processor: NMI');
    }

    // Register ACH processor
    if (config.ach.odfiRouting) {
      this.achProcessor = new AchProcessor();
      logger.info('Registered ACH processor: Direct NACHA');
    }

    // Add more processors here:
    // if (config.processors.tsys.apiKey) { ... }
    // if (config.processors.fiserv.apiKey) { ... }

    if (this.cardProcessors.size === 0) {
      logger.warn('No card processors configured — card transactions will fail');
    }
    if (!this.achProcessor) {
      logger.warn('No ACH processor configured — ACH transactions will fail');
    }
  }

  getCardProcessor(id?: string): BaseProcessor {
    const processorId = id || this.defaultCardProcessor;
    const processor = this.cardProcessors.get(processorId);
    if (!processor) {
      throw new Error(`Card processor not found: ${processorId}`);
    }
    return processor;
  }

  getAchProcessor(): BaseAchProcessor {
    if (!this.achProcessor) {
      throw new Error('ACH processor not configured');
    }
    return this.achProcessor;
  }

  listProcessors(): { card: string[]; ach: boolean } {
    return {
      card: Array.from(this.cardProcessors.keys()),
      ach: !!this.achProcessor,
    };
  }
}

export const processors = new ProcessorRegistry();
