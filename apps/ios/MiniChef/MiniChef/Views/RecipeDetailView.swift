//
//  RecipeView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//

import SwiftUI
import SwiftData

struct RecipeDetailView: View {
    let recipeID: UUID
    @Query private var  recipes: [Recipe]

    init(recipeID: UUID) {
        self.recipeID = recipeID

        _recipes = Query(filter: #Predicate<Recipe> { recipe in
            recipe.id == recipeID
        })
    }

    var body: some View {
        VStack(spacing: 12) {
            Text("Hello from RecipeDetailView mate")

            if let recipe = recipes.first {
                Text(recipe.title)
                    .font(.largeTitle)
                    .bold()
                Text(recipe.desc)
                    .foregroundStyle(.secondary)
            } else {
                ContentUnavailableView("Not Found", systemImage: "questionmark")
            }
        }
    }
}

