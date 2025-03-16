import { Component, ElementRef, ViewChild } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { HttpClient } from '@angular/common/http';
import { VerifyLinkService } from '../../services/verify-link.service';
import { MatDialog } from '@angular/material/dialog';
import { DialogComponent } from '../dialog/dialog.component';

@Component({
  selector: 'app-verify-link',
  standalone: false,
  templateUrl: './verify-link.component.html',
  styleUrls: ['./verify-link.component.css']
})
export class VerifyLinkComponent {
  articleLink = '';
  selected_type: string = '';
  selectedImage: string | null = null; // To store the image preview URL
  files: File[] = []; // To store the selected file(s)
  videoFile: File | null = null;
  videoUrl: string | null = null;

  @ViewChild('fileUpload') fileUpload!: ElementRef;

  constructor(
    private sanitizer: DomSanitizer,
    private http: HttpClient,
    private linkService: VerifyLinkService,
    private dialog: MatDialog
  ) {}

  // Trigger file input click
  onClick(event: Event) {
    if (this.fileUpload) {
      this.fileUpload.nativeElement.click();
    }
  }

  // Handle file selection
  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.files = [file]; // Store the selected file
      this.selectedImage = URL.createObjectURL(file); // Create a preview URL
    }
  }

  // Upload the selected image
  onUpload(): void {
    if (this.files.length === 0) {
      return;
    }

    const formData = new FormData();
    formData.append('files', this.files[0]);

    this.linkService.uploadFile(formData).subscribe({
      next: (response: any) => {
        console.log('Upload successful!', response);
        this.openDialog('Image uploaded successfully!');
      },
      error: (error: any) => {
        console.error('Upload failed!', error);
        this.openDialog('Upload failed: ' + error.message);
      }
    });
  }

  // Clear the selected image
  clearImage(): void {
    this.selectedImage = null;
    this.files = [];
    if (this.fileUpload) {
      this.fileUpload.nativeElement.value = ''; // Clear the file input
    }
  }

  // Clear the article link input
  clearArticleLink(): void {
    this.articleLink = '';
  }

  // Handle video file selection
  onVideoSelected(event: any) {
    if (event.target.files.length > 0) {
      this.videoFile = event.target.files[0];
    }
  }

  // Upload the selected video
  onUploadVideo() {
    if (!this.videoFile) {
      console.error('No video file selected!');
      return;
    }

    const formData = new FormData();
    formData.append('video', this.videoFile);

    this.http.post('http://localhost:5000/api/upload/video', formData).subscribe({
      next: (response) => {
        console.log('Upload successful!', response);
      },
      error: (err) => {
        console.error('Upload failed!', err);
      }
    });
  }

  // Open a dialog with a message
  openDialog(message: string): void {
    this.dialog.open(DialogComponent, {
      data: { message },
      width: '400px'
    });
  }

  // Handle confirmation based on the selected type
  onConfirm(link: string): void {
    if (this.selected_type === 'article') {
      this.verify_site_link(link);
    } else if (this.selected_type === 'image') {
      this.verify_image_link(link);
    } else if (this.selected_type === 'video') {
      this.verify_video_link(link);
    }
  }

  // Verify site link
  verify_site_link(link: string): void {
    this.linkService.verifySite(link).subscribe({
      next: (response: any) => {
        this.openDialog('Article result: ' + response['verdict']);
      },
      error: (error: any) => {
        console.error(error);
        this.openDialog('Verification failed: ' + error.message);
      }
    });
  }

  // Verify image link
  verify_image_link(link: string): void {
    this.linkService.verifyImage(link).subscribe({
      next: (response: any) => {
        this.openDialog('Image result: ' + response['prediction']);
      },
      error: (error: any) => {
        console.error(error);
        this.openDialog('Verification failed: ' + error.message);
      }
    });
  }

  // Verify video link
  verify_video_link(link: string): void {
    this.linkService.verifyVideo(link).subscribe({
      next: (response: any) => {
        this.openDialog('Provided video is ' + response['video'] + ' with ' + response['audio'] + ' criteria.');
      },
      error: (error: any) => {
        console.error(error);
        this.openDialog('Verification failed: ' + error.message);
      }
    });
  }
}