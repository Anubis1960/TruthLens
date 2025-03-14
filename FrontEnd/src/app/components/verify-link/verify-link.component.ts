import { Component } from '@angular/core';

@Component({
  selector: 'app-verify-link',
  standalone: false,
  templateUrl: './verify-link.component.html',
  styleUrl: './verify-link.component.css'
})
export class VerifyLinkComponent {
csvInputChange($event: Event) {
throw new Error('Method not implemented.');
}
  value = '';
  selected_type: string = '';
  constructor(){}

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
