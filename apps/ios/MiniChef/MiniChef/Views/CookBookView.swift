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
                NavigationLink("Recipe 1", value: NavigationPage.recipeDetail)
                NavigationLink("Recipe 2", value: NavigationPage.recipeDetail)
                NavigationLink("Recipe 3", value: NavigationPage.recipeDetail)
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
