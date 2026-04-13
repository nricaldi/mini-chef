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
                    NavigationLink(value: NavigationPage.recipeDetail(recipeID: recipe.id), label: {
                        VStack {
                            Text(recipe.title)
                                .font(.title2)
                                .bold()
                            Text(recipe.desc)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        .padding(8)
                        .frame(maxWidth: .infinity)
                        .background(.red)
                        .cornerRadius(12)
                    })
                    .buttonStyle(.plain)
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
