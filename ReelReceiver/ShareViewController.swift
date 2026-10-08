//
//  ShareViewController.swift
//  ReelReceiver
//
//  Created by Nico Ricaldi on 10/5/26.
//

import UIKit
import Social

class ShareViewController: SLComposeServiceViewController {
// class ShareViewController: NSViewController {

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

}
