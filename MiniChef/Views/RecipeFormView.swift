//
//  RecipeFormView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//
import SwiftUI
import SwiftData

struct RecipeDraft {
    var title: String
    var description: String
    var ingredients: [String]
    var steps: [String]
}

struct RecipeFormView: View {
    @State private var draft: RecipeDraft

    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let recipe: Recipe?

    init(recipe: Recipe? = nil) {
        let draft = RecipeDraft(
            title: recipe?.title ?? "",
            description: recipe?.desc ?? "",
            ingredients: recipe?.ingredients ?? [],
            steps: recipe?.steps ?? []
        )

        _draft = State(initialValue: draft)
        self.recipe = recipe
    }

    var body: some View {
        VStack(spacing: 16) {
            Text(!draft.title.isEmpty ? draft.title : "New Recipe")
                .padding(.horizontal, 16)
                .font(.title)
                .bold()

            Form {
                Section(header: Text("Title")) {
                    TextField("Grandma's classic ra...", text: $draft.title)
                }

                Section(header: Text("Description")) {
                    TextField("The best ting ever!", text: $draft.description)
                }

                Section(header: Text("Ingredients")) {
                    ForEach(0..<draft.ingredients.count, id: \.self) { index in
                        TextField("Ingredient \(index + 1)", text: $draft.ingredients[index])
                    }
                    Button("Add Ingredient") {
                        draft.ingredients.append("")
                    }
                }

                Section(header: Text("Steps")) {
                    ForEach(0..<draft.steps.count, id: \.self) { index in
                        TextField("Step \(index + 1)", text: $draft.steps[index])
                    }
                    Button("Add Step") {
                        draft.steps.append("")
                    }
                }
            }

            Button("Save Recipe") { saveRecipe() } .buttonStyle(.glassProminent)
                .disabled(draft.title.isEmpty || draft.description.isEmpty || draft.ingredients.isEmpty || draft.steps.isEmpty)
        }
        .padding(.top, 16)
    }

    func saveRecipe() {
        if let recipe {
            recipe.title = draft.title
            recipe.desc = draft.description
            recipe.ingredients = draft.ingredients
            recipe.steps = draft.steps
        } else {
            let newRecipe = Recipe(
                title: draft.title,
                desc: draft.description,
                ingredients: draft.ingredients,
                steps: draft.steps
            )
            modelContext.insert(newRecipe)
        }
        dismiss()
    }
}
