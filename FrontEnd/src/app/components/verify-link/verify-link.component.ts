import { Component, ElementRef, Input, input, ViewChild } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { HttpClient} from '@angular/common/http';
import { VerifyLinkService } from '../../services/verify-link.service';
import { DialogComponent } from '../dialog/dialog.component';
import { MatDialog } from '@angular/material/dialog';
@Component({
  selector: 'app-verify-link',
  standalone: false,
  templateUrl: './verify-link.component.html',
  styleUrl: './verify-link.component.css'
})
export class VerifyLinkComponent {
  accept: any;
  deleteButtonLabel: any;
  event: any;
  articleLink = '';
  selected_type: string = '';
  @ViewChild('fileUpload')
  fileUpload: ElementRef | undefined;
  inputFileName: string | undefined;
  @Input()
  files: File[] = []
  videoFile: File | null = null;
  videoUrl: string | null = null;
  constructor(private sanitizer: DomSanitizer, private http: HttpClient, private linkService: VerifyLinkService, private dialog: MatDialog){}

  onClick(event: Event) {
    if (this.fileUpload)
      this.fileUpload.nativeElement.click()
  }

  onInput(event: Event) {

  }
  
  onFileSelected(event: any) {
      this.files = event.target.files
  }

  onUpload(): void{
    const fd = new FormData()
    
    if (this.files.length === 0) {
      return
    }
    
    for (const file of this.files) {
      console.log(`Adăugat fișier: ${file.name}`); 
      fd.append('files', file)
    }

    this.linkService.uploadFile(fd).subscribe(
      (response: any) => {
        console.log(response);
      },

      (error: any) => {
        console.error(error);
      }
    )

  }

  onVideoSelected(event: any) {
    if (event.target.files.length > 0) {
      this.videoFile = event.target.files[0];
    }
  }

  onUploadVideo() {
    if (!this.videoFile) {
      console.error('Niciun fișier video selectat!');
      return;
    }

    const formData = new FormData();
    formData.append('video', this.videoFile);

    this.http.post('http://localhost:5000/api/upload/video', formData).subscribe({
      next: (response) => {
        console.log('Upload reușit!', response);
      },
      error: (err) => {
        console.error('Eroare la upload!', err);
      }
    });
  }

  removeFile(event:Event, file: any) {
    let ix
    if (this.files && -1 !== (ix = this.files.indexOf(file))) {
      this.files.splice(ix, 1)
      this.clearInputElement()
    }
  }
  clearArticleLink(): void {
    this.articleLink = '';
  }
  validate(file: File) {
    for (const f of this.files) {
      if (f.name === file.name
        && f.lastModified === file.lastModified
        && f.size === f.size
        && f.type === f.type) 
      {
        return false
      }
    }
    return true
  }

  clearInputElement() {
    if (this.fileUpload) {
      this.fileUpload.nativeElement.value = ''
    }
  }

  isMultiple(): boolean {
      return true; 
  }

  onConfirm(link: string):void{
    if(this.selected_type == 'article'){
      this.verify_site_link(link);

    } else if(this.selected_type == 'image'){
      this.verify_image_link(link);
    
    } else if(this.selected_type == 'video'){
      this.verify_video_link(link);
    }
  }

  verify_site_link(link: string):void {
    this.linkService.verifySite(link).subscribe({
      next: (response: any) => {
        this.openDialog("The site is verified: " + response.message);      
      },
      error: (error: any) => {
        console.log(error);
        this.openDialog("Verification failed: " + error.message);
      }
    })
  }

  openDialog(message: string): void {
    console.log("Open dialog ba");
    this.dialog.open(DialogComponent, {
      data: { message },
      width: '400px'
    });
  }

  verify_image_link(link: string):void {
    this.linkService.verifyImage(link).subscribe({
      next: (response: any) => {
        this.openDialog("The image is verified: " + response.message);      
      },
      error: (error: any) => {
        console.error(error);
        this.openDialog("Verification failed: " + error.message);
      }
    })
  }

  verify_video_link(link: string):void {
    this.linkService.verifyVideo(link).subscribe({
      next: (response: any) => {
        console.log(response);
        this.openDialog("The video is verified: " + response.message);      
      },

      error: (error: any) => {
        console.error(error);
        this.openDialog("Verification failed: " + error.message);
      }
    })
  }

}
