import { Component, ElementRef, Input, input, ViewChild } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { HttpClient} from '@angular/common/http';
import { VerifyLinkService } from '../../services/verify-link.service';
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

  value = '';
  selected_type: string = '';
@ViewChild('fileUpload')
  fileUpload: ElementRef | undefined;
  inputFileName: string | undefined;
@Input()
files: File[] = []

  constructor(private sanitizer: DomSanitizer, private http: HttpClient, private service: VerifyLinkService){}

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
    this.service.uploadFile(fd).subscribe((response) => {
      console.log(response)
    })

  }

  removeFile(event:Event, file: any) {
    let ix
    if (this.files && -1 !== (ix = this.files.indexOf(file))) {
      this.files.splice(ix, 1)
      this.clearInputElement()
    }
  }

  validate(file: File) {
    for (const f of this.files) {
      if (f.name === file.name
        && f.lastModified === file.lastModified
        && f.size === f.size
        && f.type === f.type
      ) {
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
  onConfirm():void{
    console.log(this.selected_type);
    if(this.selected_type == 'one'){
      this.verify_site_link();
    }else if(this.selected_type == 'two'){
      this.verify_image_link();
    }else if(this.selected_type == 'three'){
      this.verify_video_link();
    }
  }

  verify_site_link():void{
    console.log("In verify_site_link function...");
  }
  verify_image_link():void{
    console.log("In verify_image_link function...");
  }
  verify_video_link():void{
    console.log("In verify_video_link function...");
  }

}
