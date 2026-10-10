//
//  ShareViewController.swift
//  ReelReceiver
//
//  Created by Nico Ricaldi on 10/5/26.
//

import UIKit
import Social

import Foundation
import UniformTypeIdentifiers


struct RequestPayload: Codable {
    let url: String
}

struct MyResponse: Codable {
    let message: String
}

class ShareViewController: SLComposeServiceViewController {
// class ShareViewController: NSViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        extractAndValidate()
    }

    override func isContentValid() -> Bool {
        // Do validation of contentText and/or NSExtensionContext attachments here

        print("Hello from isContentValid")

        return true
    }

    override func didSelectPost() {
        // This is called after the user selects Post. Do the upload of contentText and/or NSExtensionContext attachments.

        print("Hello from didSelectPost")

        guard let items:[Any] = self.extensionContext?.inputItems else {
            print("Hello from guard")
            super.didSelectPost()
            return
        }

        for item in items {
            print(item)
        }

        // Inform the host that we're done, so it un-blocks its UI. Note: Alternatively you could call super's -didSelectPost,
        // which will similarly complete the extension context.
        self.extensionContext!.completeRequest(returningItems: [], completionHandler: nil)
    }

    override func configurationItems() -> [Any]! {
        // To add configuration options via table cells at the bottom of the sheet, return an array of SLComposeSheetConfigurationItem here.
        return []
    }

    private func extractAndValidate() {
        print("Hello from extractAndValidate")
        // guard let items:[NSExtensionItem] = self.extensionContext?.inputItems else { return }
        guard let items = extensionContext?.inputItems as? [NSExtensionItem] else { return }

        for item in items {
            guard let attachments = item.attachments else { continue }

            for provider in attachments {
                if !provider.hasItemConformingToTypeIdentifier(UTType.url.identifier) { return }

                provider.loadItem(forTypeIdentifier: UTType.url.identifier, options: nil) { [weak self] (item, error) in
                    guard let self = self, let url = item as? URL else { return }
                    self.postUrl(url: url)
                }

                return
            }
        }
    }

    private func postUrl(url: URL) {
        print("Hello from postUrl")
        // Might need to wrap url string in URL(string: value!)
        var request = URLRequest(url: URL(string: "https://mini-chef.fastapicloud.dev/process-video")!)
        request.httpMethod = "POST"

        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        let body: [String: String] = ["url": url.absoluteString]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            print("Hello from inside URLSession")
            print("Here is the data: \(data)")

            if let responseData = data {
                do {
                    let decodedObject = try JSONDecoder().decode(MyResponse.self, from: responseData)
                    print("Decoded Data: \(decodedObject)")
                } catch {
                    print("Failed to decode JSON: \(error)")
                }
            }

            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                print(httpResponse)
            } else {
                print("Request Failed")
            }

        }.resume()
    }
}
