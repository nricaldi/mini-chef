//
//  RecipeView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//

import SwiftUI

struct RecipeDetailView: View {
    var recipeID: UUID

    var body: some View {
        VStack(spacing: 12) {
            Text("Hello from RecipeDetailView mate")
            Text("Currently viewing \(recipeID)")
        }
    }
}

