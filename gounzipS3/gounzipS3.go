package main

import (
	"archive/zip"
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
)

//Event Input event for Golang unzip Function.
type Event struct {
        src string `json:"src"`
        dst string `json:"dst"`
        zip string `json:"zip"`
}

//Dependencies session injection
type Dependencies struct {
	session session.Session 
}

//HandleRequest - Main entry point for lambda
func (d *Dependencies) HandleRequest(ctx context.Context, event Event) (string, error) {

	src := event.src
	dst := event.dst
	zipFile := event.zip

	file, err := os.Create(zipFile)
	if(err != nil){
		fmt.Println(err)
	}


    downloader := s3manager.NewDownloader(&d.session)
	_, err = downloader.Download(file, &s3.GetObjectInput{
		Bucket: aws.String(src),
		Key: aws.String(zipFile),
	})

	if err != nil{
		fmt.Println("Error fetching src file {} from bucket {}", zipFile, src);
	}
	
	//Begin unzip and write of files and folders.

	reader, err := zip.OpenReader(file.Name())
	if err != nil{

	}
	defer reader.Close()
	uploader := s3manager.NewUploader(&d.session)

	uploader.Upload(&s3manager.UploadInput{})
	// Iterate through the files in the archive
	for _, f := range reader.File {
		
		rc, err := f.Open()
		if err != nil {
			log.Fatal(err)
		}
		
		uploader.Upload(&s3manager.UploadInput{
			Bucket: aws.String(dst),
			Key: aws.String(zipFile),
			Body: rc,
		})
		
		if err != nil {
			log.Fatal(err)
		}
		rc.Close()
		fmt.Println()
	}
	return "{\"Unziped\": true}", nil
}

func main() {

	d := Dependencies{
		session: *session.New(),
	}
    //Dependency injection with the pointer receiver
	lambda.Start(d.HandleRequest)
}
