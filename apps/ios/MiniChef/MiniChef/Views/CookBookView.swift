//
//  CookBookView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//

import SwiftUI
import SwiftData

struct CookBookView: View {
    @Query private var recipes: [Recipe]
    @State private var showSheet: Bool = false

    var body: some View {
        VStack {
            Text("Your recipes:")
            VStack(spacing: 12) {
                ForEach(recipes) { recipe in
                    VStack {
                        Text(recipe.title)
                            .font(.title2)
                            .bold()
                        Text(recipe.desc)
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                    .padding(8)
                    .background(.red)
                    .cornerRadius(12)
//                    NavigationLink(recipe.title, value: NavigationPage.recipeDetail)
                }
            }
            .padding(16)

            Button ("\(Image(systemName: "plus.circle.fill")) New Recipe") {
                showSheet.toggle()
            }
            .sheet(isPresented: $showSheet) {
                RecipeFormView()
            }
        }
    }
}
