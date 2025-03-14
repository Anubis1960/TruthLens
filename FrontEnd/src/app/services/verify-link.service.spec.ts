import { TestBed } from '@angular/core/testing';

import { VerifyLinkService } from './verify-link.service';

describe('VerifyLinkService', () => {
  let service: VerifyLinkService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VerifyLinkService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
