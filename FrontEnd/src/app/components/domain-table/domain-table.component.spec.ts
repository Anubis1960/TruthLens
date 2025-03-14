import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DomainTableComponent } from './domain-table.component';

describe('DomainTableComponent', () => {
  let component: DomainTableComponent;
  let fixture: ComponentFixture<DomainTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DomainTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DomainTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
