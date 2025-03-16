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
  selectedImage: string | null = null; // For image preview
  files: File[] = []; // For image upload
  videoFile: File | undefined; // For video upload
  videoUrl: string | null = null; // For video preview
  isUploading: boolean = false; // Loading state for image upload
  isUploadingVideo: boolean = false; // Loading state for video upload
  isVerifying: boolean = false; // Loading state for link verification

  @ViewChild('fileUpload') fileUpload!: ElementRef;
  @ViewChild('videoUpload') videoUpload!: ElementRef;

  constructor(
    private sanitizer: DomSanitizer,
    private http: HttpClient,
    private linkService: VerifyLinkService,
    private dialog: MatDialog
  ) {}

  // Trigger file input click for images
  onClick(event: Event): void {
    if (this.fileUpload) {
      this.fileUpload.nativeElement.click();
    }
  }

  // Trigger file input click for videos
  onClickVideoUpload(event: Event): void {
    if (this.videoUpload) {
      this.videoUpload.nativeElement.click();
    }
  }

  // Handle image file selection
  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.files = [file]; // Store the selected file
      this.selectedImage = URL.createObjectURL(file); // Create a preview URL
    }
  }

  // Handle video file selection
  onVideoSelected(event: any): void {
    if (event.target.files.length > 0) {
      this.videoFile = event.target.files[0];
      this.videoUrl = URL.createObjectURL(this.videoFile!); // Create a preview URL
    }
  }

  // Clear the selected image
  clearImage(): void {
    this.selectedImage = null;
    this.files = [];
    if (this.fileUpload) {
      this.fileUpload.nativeElement.value = ''; // Reset the file input
    }
  }

  // Clear the selected video
  clearVideoInput(): void {
    this.videoFile = undefined ;
    this.videoUrl = null;
    if (this.videoUpload) {
      this.videoUpload.nativeElement.value = ''; // Reset the file input
    }
  }

  // Clear the article link input
  clearArticleLink(): void {
    this.articleLink = '';
    this.selected_type = '';
  }

  // Upload the selected image
  onUpload(): void {
    if (this.files.length === 0) {
      return;
    }

    this.isUploading = true; // Set loading state to true

    const formData = new FormData();
    formData.append('files', this.files[0]);

    this.linkService.uploadFile(formData).subscribe({
      next: (response: any) => {
        this.openDialog('Image uploaded successfully!').afterClosed().subscribe(() => {
          this.clearImage(); // Clear the image after the dialog is closed
          this.isUploading = false; // Reset loading state
        });
      },
      error: (error: any) => {
        this.openDialog('Upload failed: ' + error.message).afterClosed().subscribe(() => {
          this.clearImage(); // Clear the image after the dialog is closed
          this.isUploading = false; // Reset loading state
        });
      }
    });
  }

  // Upload the selected video
  onUploadVideo(): void {
    if (!this.videoFile) {
      console.error('No video file selected!');
      return;
    }

    this.isUploadingVideo = true; // Set loading state to true

    const formData = new FormData();
    formData.append('video', this.videoFile);

    this.http.post('http://localhost:5000/api/upload/video', formData).subscribe({
      next: (response: any) => {
        this.openDialog('Video uploaded successfully!').afterClosed().subscribe(() => {
          this.clearVideoInput(); // Clear the video after the dialog is closed
          this.isUploadingVideo = false; // Reset loading state
        });
      },
      error: (err) => {
        this.openDialog('Upload failed: ' + err.message).afterClosed().subscribe(() => {
          this.clearVideoInput(); // Clear the video after the dialog is closed
          this.isUploadingVideo = false; // Reset loading state
        });
      }
    });
  }

  // Handle confirmation based on the selected type
  onConfirm(link: string): void {
    if (!link || !this.selected_type) {
      return;
    }

    this.isVerifying = true; // Set loading state to true

    if (this.selected_type === 'article') {
      this.verify_site_link(link).subscribe({
        next: (response: any) => {
          this.openDialog("Article result: " + response['verdict']).afterClosed().subscribe(() => {
            this.clearArticleLink(); // Clear the link input after the dialog is closed
            this.isVerifying = false; // Reset loading state
          });
        },
        error: (error: any) => {
          this.openDialog("Verification failed: " + error.message).afterClosed().subscribe(() => {
            this.clearArticleLink(); // Clear the link input after the dialog is closed
            this.isVerifying = false; // Reset loading state
          });
        }
      });
    } else if (this.selected_type === 'image') {
      this.verify_image_link(link).subscribe({
        next: (response: any) => {
          this.openDialog("Image result: " + response['prediction']).afterClosed().subscribe(() => {
            this.clearArticleLink(); // Clear the link input after the dialog is closed
            this.isVerifying = false; // Reset loading state
          });
        },
        error: (error: any) => {
          this.openDialog("Verification failed: " + error.message).afterClosed().subscribe(() => {
            this.clearArticleLink(); // Clear the link input after the dialog is closed
            this.isVerifying = false; // Reset loading state
          });
        }
      });
    } else if (this.selected_type === 'video') {
      this.verify_video_link(link).subscribe({
        next: (response: any) => {
          this.openDialog("Provided video is " + response['video'] + " with " + response['audio'] + " criteria.").afterClosed().subscribe(() => {
            this.clearArticleLink(); // Clear the link input after the dialog is closed
            this.isVerifying = false; // Reset loading state
          });
        },
        error: (error: any) => {
          this.openDialog("Verification failed: " + error.message).afterClosed().subscribe(() => {
            this.clearArticleLink(); // Clear the link input after the dialog is closed
            this.isVerifying = false; // Reset loading state
          });
        }
      });
    }
  }

  // Open a dialog with a message
  openDialog(message: string): any {
    return this.dialog.open(DialogComponent, {
      data: { message },
      width: '400px'
    });
  }

  // Verify site link
  verify_site_link(link: string): any {
    return this.linkService.verifySite(link);
  }

  // Verify image link
  verify_image_link(link: string): any {
    return this.linkService.verifyImage(link);
  }

  // Verify video link
  verify_video_link(link: string): any {
    console.log(link)
    return this.linkService.verifyVideo(link);
  }
}