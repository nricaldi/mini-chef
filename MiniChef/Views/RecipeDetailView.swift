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
    @Query private var recipes: [Recipe]

    init(recipeID: UUID) {
        self.recipeID = recipeID

        _recipes = Query(filter: #Predicate<Recipe> { recipe in
            recipe.id == recipeID
        })
    }

    var body: some View {
        if let recipe = recipes.first {
            VStack {
                Text(recipe.title)
                    .font(.largeTitle)
                    .bold()
                Text(recipe.desc)
                    .foregroundStyle(.secondary)

                List {
                    Section(header: Text("Ingredients")) {
                        ForEach(recipe.ingredients, id: \.self) { ingredient in
                            Text(ingredient)
                        }
                    }

                    Section(header: Text("Steps")) {
                        ForEach(0..<recipe.steps.count, id: \.self) { index in
                            HStack {
                                Text("\(index + 1).")
                                Text(recipe.steps[index])
                            }
                        }
                    }
                }
            }
            .toolbar {
                ToolbarItem {
                    NavigationLink("Edit", value: NavigationPage.recipeEdit(recipe: recipe))
                }
            }
        } else {
            ContentUnavailableView("Not Found", systemImage: "questionmark")
        }
    }
}

