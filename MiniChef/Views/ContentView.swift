//
//  ContentView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//

import SwiftUI

enum NavigationPage: Hashable {
    case recipeEdit(recipe: Recipe)
    case recipeDetail(recipeID: UUID)
}

struct ContentView: View {
    var body: some View {
        NavigationStack {
            CookBookView()
            .buttonStyle(.glassProminent)
            .navigationTitle("Mini chef")
            .navigationDestination(for: NavigationPage.self) { page in
                switch page {
                    case .recipeEdit(let recipe): RecipeFormView(recipe: recipe)
                    case .recipeDetail(let recipeID): RecipeDetailView(recipeID: recipeID)
                }
            }
        }
    }
}

#Preview {
    ContentView()
}
