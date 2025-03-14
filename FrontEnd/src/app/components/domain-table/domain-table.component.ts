import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort, Sort } from '@angular/material/sort';
import { LiveAnnouncer } from '@angular/cdk/a11y';

@Component({
  selector: 'app-domain-table',
  standalone: false,
  templateUrl: './domain-table.component.html',
  styleUrls: ['./domain-table.component.css']
})
export class DomainTableComponent implements AfterViewInit {
  displayedColumns: string[] = ['domain', 'trustRate']; 
  dataSource: MatTableDataSource<any>;
  data = [
    { domain: 'example.com', trustRate: 95 },
    { domain: 'suspicious-site.net', trustRate: 30 },
    { domain: 'trustedsource.org', trustRate: 85 },
  ];

  @ViewChild(MatSort) sort!: MatSort;

  constructor(private _liveAnnouncer: LiveAnnouncer) {
    this.dataSource = new MatTableDataSource(this.data);
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  announceSortChange(sortState: Sort) {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }
}
