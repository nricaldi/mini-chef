//
//  RecipeFormView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//
import SwiftUI

struct RecipeFormView: View {
    @State private var title: String = ""
    @State private var description: String = ""

    @State private var ingredients: [String]  = [""]
    @State private var steps: [String]  = [""]

    var body: some View {
        Text(title.isEmpty ? "New Recipe" : title)
            .padding([.top, .horizontal], 16)
            .font(.title)
            .bold()

        Form {
            Section(header: Text("Title")) {
                TextField("Grandma's classic ra...", text: $title)
            }

            Section(header: Text("Description")) {
                TextField("The best ting ever!", text: $description)
            }

            Section(header: Text("Ingredients")) {
                ForEach(0..<ingredients.count, id: \.self) { index in
                    TextField("Ingredient \(index + 1)", text: $ingredients[index])
                }
                Button("Add Item") {
                    ingredients.append("")
                }
            }

            Section(header: Text("Steps")) {
                ForEach(0..<steps.count, id: \.self) { index in
                    TextField("Step \(index + 1)", text: $steps[index])
                }
                Button("Add Item") {
                    steps.append("")
                }
            }
        }
    }
}
