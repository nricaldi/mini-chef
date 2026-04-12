//
//  ContentView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//

import SwiftUI

enum NavigationPage {
    case recipeDetail
}

struct ContentView: View {
    var body: some View {
        NavigationStack {
            CookBookView()
            .buttonStyle(.glassProminent)
            .navigationTitle("Mini chef")
            .navigationDestination(for: NavigationPage.self) { page in
                switch page {
                    case .recipeDetail: RecipeDetailView()
                }
            }
        }
    }
}

#Preview {
    ContentView()
}
