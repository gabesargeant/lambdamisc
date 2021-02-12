package main

import (
	"context"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
)

//Event Input event for Golang unzip Function.
type Event struct {
        src string `json:"src"`
        dst string `json:"dst"`
        zip string `json:"zip"`
}
//HandleRequest - Main entry point for lambda
func (d *Dependencies) HandleRequest(ctx context.Context, name event) (string, error) {

	src := event["src"]
	dst := event["dst"]
	zip := event["zip"]


        downloader := s3manager.NewDownloader(d.session)

	

}

func main() {

	d := Dependencies{
		session: session.Must(session.NewSession()),
	}
        //Dependency injection with pointer receivers!
	lambda.Start(d.HandleRequest)
}
