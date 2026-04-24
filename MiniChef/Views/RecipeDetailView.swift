//
//  RecipeView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//

import SwiftUI
import SwiftData

struct RecipeDetailView: View {
    @State private var isShowingConfirm = false

    @Query private var recipes: [Recipe]

    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    init(recipeID: UUID) {
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
                    NavigationLink(value: NavigationPage.recipeEdit(recipe: recipe)) {
                        Image(systemName: "square.and.pencil")
                    }
                }
                ToolbarSpacer(.fixed)
                ToolbarItem {
                    Button(action: showConfirm) {
                        Image(systemName: "trash")
                    }
                    .confirmationDialog(
                        "Are you sure?",
                        isPresented: $isShowingConfirm,
                        titleVisibility: .visible
                    ) {
                        Button("Yes, delete", role: .destructive) { delete() }
                        Button("No, I want to keep it", role: .cancel) { }
                    } message: {
                        Text("This action cannot be reverted")
                    }
                }
            }
        } else {
            ContentUnavailableView("Not Found", systemImage: "questionmark")
        }
    }

    func delete() {
        if let recipe = recipes.first {
            modelContext.delete(recipe)
            dismiss()
        }
    }

    func showConfirm() {
        isShowingConfirm = true
    }
}

